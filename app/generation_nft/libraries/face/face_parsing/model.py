# -*- coding: utf-8 -*-
r"""
.-----------------------------------------------------.

______                           _           _
| ___ \                         | |         (_)
| |_/ / __ ___  _ __   ___   ___| |__   __ _ _ _ __
|  __/ '__/ _ \| '_ \ / _ \ / __| '_ \ / _` | | '_ \
| |  | | | (_) | | | | (_) | (__| | | | (_| | | | | |
\_|  |_|  \___/|_| |_|\___/ \___|_| |_|\__,_|_|_| |_|


.-----------------------------------------------------.

 _____                           _   _               _   _ ______ _____
|  __ \                         | | (_)             | \ | ||  ___|_   _|
| |  \/ ___ _ __   ___ _ __ __ _| |_ _  ___  _ __   |  \| || |_    | |
| | __ / _ \ '_ \ / _ \ '__/ _` | __| |/ _ \| '_ \  | . ` ||  _|   | |
| |_\ \  __/ | | |  __/ | | (_| | |_| | (_) | | | | | |\  || |     | |
 \____/\___|_| |_|\___|_|  \__,_|\__|_|\___/|_| |_| \_| \_/\_|     \_/


.------------------------------------------------------------------------.

File: app/generation_nft/libraries/face/face_parsing/model.py
"""
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.model_zoo as modelzoo

from app.settings import settings


class ConvBNReLU(nn.Module):
    """Classe ConvBNReLU.

    Args:
        nn.Module (nn.Module): nn.Module.
    """

    def __init__(
        self,
        in_chan: int,
        out_chan: int,
        ks: int = 3,
        stride: int = 1,
        padding: int = 1,
    ):
        """Initialise la classe ConvBNReLU.

        Args:
            in_chan (int): nombre de canal d'entré.
            out_chan (int): nombre de canal de sorti.
            ks (int, optional): kernel_size. Défaut à 3.
            stride (int, optional): stride. Défaut à 1.
            padding (int, optional): padding. Défaut à 1.
        """
        super(ConvBNReLU, self).__init__()
        self.conv = nn.Conv2d(
            in_chan,
            out_chan,
            kernel_size=ks,
            stride=stride,
            padding=padding,
            bias=False,
        )
        self.bn = nn.BatchNorm2d(out_chan)
        self.init_weight()

    def forward(self, x: np.array) -> F.relu:
        """Forward.

        Args:
            x (np.array): x.

        Returns:
            F.relu: F.relu.
        """
        return F.relu(self.bn(self.conv(x)))

    def init_weight(self):
        """Initialise le poids."""
        for ly in self.children():
            if isinstance(ly, nn.Conv2d):
                nn.init.kaiming_normal_(ly.weight, a=1)
                if ly.bias is not None:
                    nn.init.constant_(ly.bias, 0)


class BiSeNetOutput(nn.Module):
    """Classe BiSeNetOutput.

    Args:
        nn.Module (nn.Module): nn.Module.
    """

    def __init__(self, in_chan: int, mid_chan: int, n_classes: int):
        """Initialise la classe BiSeNetOutput.

        Args:
            in_chan (int): nombre de canal d'entré.
            mid_chan (int): nombre de canal de sorti.
            n_classes (int): nombre de classes à détectées.
        """
        super(BiSeNetOutput, self).__init__()
        self.conv = ConvBNReLU(in_chan, mid_chan, ks=3, stride=1, padding=1)
        self.conv_out = nn.Conv2d(mid_chan, n_classes, kernel_size=1, bias=False)
        self.init_weight()

    def forward(self, x: np.array) -> np.array:
        """Forward.

        Args:
            x (np.array): x.

        Returns:
            np.array: conv out.
        """
        return self.conv_out(self.conv(x))

    def init_weight(self):
        """Initialise le poids."""
        for ly in self.children():
            if isinstance(ly, nn.Conv2d):
                nn.init.kaiming_normal_(ly.weight, a=1)
                if ly.bias is not None:
                    nn.init.constant_(ly.bias, 0)

    def get_params(self) -> tuple:
        """Récupère les paramètres du modèle.

        Returns:
            tuple: weight decay paramètre, no_weight_decay paramètre.
        """
        wd_params, nowd_params = [], []
        for _, module in self.named_modules():
            if isinstance(module, nn.Linear) or isinstance(module, nn.Conv2d):
                wd_params.append(module.weight)
                if module.bias is not None:
                    nowd_params.append(module.bias)
            elif isinstance(module, nn.BatchNorm2d):
                nowd_params += list(module.parameters())
        return wd_params, nowd_params


class AttentionRefinementModule(nn.Module):
    """Classe AttentionRefinementModule.

    Args:
        nn.Module (nn.Module): nn.Module.
    """

    def __init__(self, in_chan: int, out_chan: int):
        """Initialise la classe AttentionRefinementModule.

        Args:
            in_chan (int): nombre de canal d'entré.
            out_chan (int): nombre de canal de sorti.
        """
        super(AttentionRefinementModule, self).__init__()
        self.conv = ConvBNReLU(in_chan, out_chan, ks=3, stride=1, padding=1)
        self.conv_atten = nn.Conv2d(out_chan, out_chan, kernel_size=1, bias=False)
        self.bn_atten = nn.BatchNorm2d(out_chan)
        self.sigmoid_atten = nn.Sigmoid()
        self.init_weight()

    def forward(self, x: np.array) -> np.array:
        """Forward.

        Args:
            x (np.array): x.

        Returns:
            np.array: torch mul.
        """
        feat = self.conv(x)
        atten = F.avg_pool2d(feat, feat.size()[2:])
        atten = self.conv_atten(atten)
        atten = self.bn_atten(atten)
        atten = self.sigmoid_atten(atten)
        return torch.mul(feat, atten)

    def init_weight(self):
        """Initialise le poids."""
        for ly in self.children():
            if isinstance(ly, nn.Conv2d):
                nn.init.kaiming_normal_(ly.weight, a=1)
                if ly.bias is not None:
                    nn.init.constant_(ly.bias, 0)


class ContextPath(nn.Module):
    """Classe ContextPath.

    Args:
        nn.Module (nn.Module): nn.Module.
    """

    def __init__(self, resnet: str):
        """Initialise la classe ContextPath.

        Args:
            resnet (str): url de téléchargement resnet.
        """
        super(ContextPath, self).__init__()
        self.resnet = Resnet18(resnet)
        self.arm16 = AttentionRefinementModule(256, 128)
        self.arm32 = AttentionRefinementModule(512, 128)
        self.conv_head32 = ConvBNReLU(128, 128, ks=3, stride=1, padding=1)
        self.conv_head16 = ConvBNReLU(128, 128, ks=3, stride=1, padding=1)
        self.conv_avg = ConvBNReLU(512, 128, ks=1, stride=1, padding=0)
        self.init_weight()

    def forward(self, x: np.array) -> tuple:
        """Forward.

        Args:
            x (np.array): x.

        Returns:
            tuple: feat 8, feat 16 up, feat 32 up.
        """
        _, _ = x.size()[2:]
        feat8, feat16, feat32 = self.resnet(x)
        H8, W8 = feat8.size()[2:]
        H16, W16 = feat16.size()[2:]
        H32, W32 = feat32.size()[2:]
        avg = F.avg_pool2d(feat32, feat32.size()[2:])
        avg = self.conv_avg(avg)
        avg_up = F.interpolate(avg, (H32, W32), mode="nearest")
        feat32_arm = self.arm32(feat32)
        feat32_sum = feat32_arm + avg_up
        feat32_up = F.interpolate(feat32_sum, (H16, W16), mode="nearest")
        feat32_up = self.conv_head32(feat32_up)
        feat16_arm = self.arm16(feat16)
        feat16_sum = feat16_arm + feat32_up
        feat16_up = F.interpolate(feat16_sum, (H8, W8), mode="nearest")
        feat16_up = self.conv_head16(feat16_up)
        return feat8, feat16_up, feat32_up

    def init_weight(self):
        """Initialise le poids."""
        for ly in self.children():
            if isinstance(ly, nn.Conv2d):
                nn.init.kaiming_normal_(ly.weight, a=1)
                if ly.bias is not None:
                    nn.init.constant_(ly.bias, 0)

    def get_params(self):
        """Récupère les paramètres du modèle.

        Returns:
            tuple: weight decay paramètre, no_weight_decay paramètre.
        """
        wd_params, nowd_params = [], []
        for _, module in self.named_modules():
            if isinstance(module, (nn.Linear, nn.Conv2d)):
                wd_params.append(module.weight)
                if module.bias is not None:
                    nowd_params.append(module.bias)
            elif isinstance(module, nn.BatchNorm2d):
                nowd_params += list(module.parameters())
        return wd_params, nowd_params


class SpatialPath(nn.Module):
    """Classe SpatialPath.

    Args:
        nn.Module (nn.Module): nn.Module.
    """

    def __init__(self):
        """Initialise la classe SpatialPath."""
        super(SpatialPath, self).__init__()
        self.conv1 = ConvBNReLU(3, 64, ks=7, stride=2, padding=3)
        self.conv2 = ConvBNReLU(64, 64, ks=3, stride=2, padding=1)
        self.conv3 = ConvBNReLU(64, 64, ks=3, stride=2, padding=1)
        self.conv_out = ConvBNReLU(64, 128, ks=1, stride=1, padding=0)
        self.init_weight()

    def forward(self, x: np.array) -> np.array:
        """Forward.

        Args:
            x (np.array): x.

        Returns:
            np.array: conv out.
        """
        feat = self.conv1(x)
        feat = self.conv2(feat)
        feat = self.conv3(feat)
        return self.conv_out(feat)

    def init_weight(self):
        """Initialise le poids."""
        for ly in self.children():
            if isinstance(ly, nn.Conv2d):
                nn.init.kaiming_normal_(ly.weight, a=1)
                if ly.bias is not None:
                    nn.init.constant_(ly.bias, 0)

    def get_params(self):
        """Récupère les paramètres du modèle.

        Returns:
            tuple: weight decay paramètre, no_weight_decay paramètre.
        """
        wd_params, nowd_params = [], []
        for _, module in self.named_modules():
            if isinstance(module, nn.Linear) or isinstance(module, nn.Conv2d):
                wd_params.append(module.weight)
                if module.bias is not None:
                    nowd_params.append(module.bias)
            elif isinstance(module, nn.BatchNorm2d):
                nowd_params += list(module.parameters())
        return wd_params, nowd_params


class FeatureFusionModule(nn.Module):
    """Classe FeatureFusionModule.

    Args:
        nn.Module (nn.Module): nn.Module.
    """

    def __init__(self, in_chan: int, out_chan: int):
        """Initialise la classe FeatureFusionModule.

        Args:
            in_chan (int): nombre de canal d'entré.
            out_chan (int): nombre de canal de sorti.
        """
        super(FeatureFusionModule, self).__init__()
        self.convblk = ConvBNReLU(in_chan, out_chan, ks=1, stride=1, padding=0)
        self.conv1 = nn.Conv2d(
            out_chan, out_chan // 4, kernel_size=1, stride=1, padding=0, bias=False
        )
        self.conv2 = nn.Conv2d(
            out_chan // 4, out_chan, kernel_size=1, stride=1, padding=0, bias=False
        )
        self.relu = nn.ReLU(inplace=True)
        self.sigmoid = nn.Sigmoid()
        self.init_weight()

    def forward(self, fsp: np.array, fcp: np.array) -> np.array:
        """Forward.

        Args:
            fsp (np.array): fsp.
            fcp (np.array): fcp.

        Returns:
            np.array: feat out.
        """
        fcat = torch.cat([fsp, fcp], dim=1)
        feat = self.convblk(fcat)
        atten = F.avg_pool2d(feat, feat.size()[2:])
        atten = self.conv1(atten)
        atten = self.relu(atten)
        atten = self.conv2(atten)
        atten = self.sigmoid(atten)
        feat_atten = torch.mul(feat, atten)
        feat_out = feat_atten + feat
        return feat_out

    def init_weight(self):
        """Initialise le poids."""
        for ly in self.children():
            if isinstance(ly, nn.Conv2d):
                nn.init.kaiming_normal_(ly.weight, a=1)
                if ly.bias is not None:
                    nn.init.constant_(ly.bias, 0)

    def get_params(self):
        """Récupère les paramètres du modèle.

        Returns:
            tuple: weight decay paramètre, no_weight_decay paramètre.
        """
        wd_params, nowd_params = [], []
        for _, module in self.named_modules():
            if isinstance(module, nn.Linear) or isinstance(module, nn.Conv2d):
                wd_params.append(module.weight)
                if module.bias is not None:
                    nowd_params.append(module.bias)
            elif isinstance(module, nn.BatchNorm2d):
                nowd_params += list(module.parameters())
        return wd_params, nowd_params


class BiSeNet(nn.Module):
    """Classe BiSeNet.

    Args:
        nn.Module (nn.Module): nn.Module.
    """

    def __init__(self, resnet: str, n_classes: int):
        """Initialise la classe BiSeNet.

        Args:
            resnet (str): url de téléchargement resnet.
            n_classes (int): nombre de classes à détectées.
        """
        super(BiSeNet, self).__init__()
        self.cp = ContextPath(resnet)
        self.ffm = FeatureFusionModule(256, 256)
        self.conv_out = BiSeNetOutput(256, 256, n_classes)
        self.conv_out16 = BiSeNetOutput(128, 64, n_classes)
        self.conv_out32 = BiSeNetOutput(128, 64, n_classes)
        self.resnet = resnet
        self.init_weight()

    def forward(self, x: np.array) -> tuple:
        """Forward.

        Args:
            x (np.array): x.

        Returns:
            tuple: feat out, feat out 16, feat out 32.
        """
        H, W = x.size()[2:]
        feat_res8, feat_cp8, feat_cp16 = self.cp(x)
        feat_sp = feat_res8
        feat_fuse = self.ffm(feat_sp, feat_cp8)
        feat_out = self.conv_out(feat_fuse)
        feat_out16 = self.conv_out16(feat_cp8)
        feat_out32 = self.conv_out32(feat_cp16)
        feat_out = F.interpolate(feat_out, (H, W), mode="bilinear", align_corners=True)
        feat_out16 = F.interpolate(
            feat_out16, (H, W), mode="bilinear", align_corners=True
        )
        feat_out32 = F.interpolate(
            feat_out32, (H, W), mode="bilinear", align_corners=True
        )
        return feat_out, feat_out16, feat_out32

    def init_weight(self):
        """Initialise le poids."""
        for ly in self.children():
            if isinstance(ly, nn.Conv2d):
                nn.init.kaiming_normal_(ly.weight, a=1)
                if ly.bias is not None:
                    nn.init.constant_(ly.bias, 0)

    def get_params(self):
        """Récupère les paramètres du modèle.

        Returns:
            tuple: weight decay paramètre, no_weight_decay paramètre.
        """
        wd_params, nowd_params, lr_mul_wd_params, lr_mul_nowd_params = [], [], [], []
        for _, child in self.named_children():
            child_wd_params, child_nowd_params = child.get_params()
            if isinstance(child, FeatureFusionModule) or isinstance(
                child, BiSeNetOutput
            ):
                lr_mul_wd_params += child_wd_params
                lr_mul_nowd_params += child_nowd_params
            else:
                wd_params += child_wd_params
                nowd_params += child_nowd_params
        return wd_params, nowd_params, lr_mul_wd_params, lr_mul_nowd_params


def conv3x3(in_planes: int, out_planes: int, stride: int = 1) -> nn.Conv2d:
    """3x3 convolution avec padding.

    Args:
        in_planes (int): nombre de canal d'entré.
        out_planes (int): nombre de canal de sorti.
        stride (int, optional): stride. Défaut à 1.

    Returns:
        nn.Conv2d: nn.Conv2d.
    """
    return nn.Conv2d(
        in_planes, out_planes, kernel_size=3, stride=stride, padding=1, bias=False
    )


class BasicBlock(nn.Module):
    """Classe BasicBlock.

    Args:
        nn.Module (nn.Module): nn.Module.
    """

    def __init__(self, in_chan: int, out_chan: int, stride: int = 1):
        """Initialise la classe BasicBlock.

        Args:
            in_chan (int): nombre de canal d'entré.
            out_chan (int): nombre de canal de sorti.
            stride (int, optional): stride. Défaut à 1.
        """
        super(BasicBlock, self).__init__()
        self.conv1 = conv3x3(in_chan, out_chan, stride)
        self.bn1 = nn.BatchNorm2d(out_chan)
        self.conv2 = conv3x3(out_chan, out_chan)
        self.bn2 = nn.BatchNorm2d(out_chan)
        self.relu = nn.ReLU(inplace=True)
        self.downsample = None
        if in_chan != out_chan or stride != 1:
            self.downsample = nn.Sequential(
                nn.Conv2d(in_chan, out_chan, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_chan),
            )

    def forward(self, x: np.array) -> np.array:
        """Forward.

        Args:
            x (np.array): x.

        Returns:
            np.array: out.
        """
        residual = self.conv1(x)
        residual = F.relu(self.bn1(residual))
        residual = self.conv2(residual)
        residual = self.bn2(residual)
        shortcut = x
        if self.downsample is not None:
            shortcut = self.downsample(x)
        out = shortcut + residual
        return self.relu(out)


def create_layer_basic(
    in_chan: int, out_chan: int, bnum: int, stride: int = 1
) -> nn.Sequential:
    """Create layer basic.

    Args:
        in_chan (int): nombre de canal d'entré.
        out_chan (int): nombre de canal de sorti.
        bnum (int): bnum.
        stride (int, optional): stride. Défaut à 1.

    Returns:
        nn.Sequential: nn.Sequential.
    """
    layers = [BasicBlock(in_chan, out_chan, stride=stride)]
    for _ in range(bnum - 1):
        layers.append(BasicBlock(out_chan, out_chan, stride=1))
    return nn.Sequential(*layers)


class Resnet18(nn.Module):
    """Classe Restnet18.

    Args:
        nn.Module (nn.Module): nn.Module.
    """

    def __init__(self, resnet: str):
        """Initialise la classe Resnet18.

        Args:
            resnet (str): url de téléchargement resnet.
        """
        super(Resnet18, self).__init__()
        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        self.layer1 = create_layer_basic(64, 64, bnum=2, stride=1)
        self.layer2 = create_layer_basic(64, 128, bnum=2, stride=2)
        self.layer3 = create_layer_basic(128, 256, bnum=2, stride=2)
        self.layer4 = create_layer_basic(256, 512, bnum=2, stride=2)
        self.resnet = resnet
        self.init_weight()

    def forward(self, x: np.array) -> tuple:
        """Forward.

        Args:
            x (np.array): x.

        Returns:
            tuple: feat 8, feat16, feat 32.
        """
        x = self.conv1(x)
        x = F.relu(self.bn1(x))
        x = self.maxpool(x)
        x = self.layer1(x)
        feat8 = self.layer2(x)
        feat16 = self.layer3(feat8)
        feat32 = self.layer4(feat16)
        return feat8, feat16, feat32

    def init_weight(self):
        """Initialise le poids."""
        state_dict = modelzoo.load_url(
            self.resnet,
            model_dir=settings.FACE_PARSING_MODEL_PATH,
            file_name=settings.RESNET_FILE,
            map_location=torch.device("cpu"),
        )
        self_state_dict = self.state_dict()
        for k, v in state_dict.items():
            if "fc" in k:
                continue
            self_state_dict.update({k: v})
        self.load_state_dict(self_state_dict)

    def get_params(self):
        """Récupère les paramètres du modèle.

        Returns:
            tuple: weight decay paramètre, no_weight_decay paramètre.
        """
        wd_params, nowd_params = [], []
        for _, module in self.named_modules():
            if isinstance(module, (nn.Linear, nn.Conv2d)):
                wd_params.append(module.weight)
                if module.bias is not None:
                    nowd_params.append(module.bias)
            elif isinstance(module, nn.BatchNorm2d):
                nowd_params += list(module.parameters())
        return wd_params, nowd_params
