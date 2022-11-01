'use strict';
import { packToFs } from 'ipfs-car/pack/fs'
import { FsBlockStore } from 'ipfs-car/blockstore/fs'
import { CarReader } from '@ipld/car/reader'
import fs from 'fs';
import express from 'express';
import bodyParser from 'body-parser'
import { NFTStorage } from 'nft.storage'
import { CID } from 'multiformats/cid'

const API_IP = process.env.API_IP != undefined ? process.env.API_IP : "localhost"
const CAR_API_PORT = process.env.CAR_API_PORT != undefined ? process.env.CAR_API_PORT : "8080"
const CAR_PATH = 'data/players.car'
const PLAYERS_PATH = 'data/players'

const app = express();
app.use(bodyParser.json({ limit: '50mb' }))

async function generate_car(req, res) {
  console.log("STARTING GENERATE CAR")
  await packToFs({
    input: PLAYERS_PATH,
    output: CAR_PATH,
    blockstore: new FsBlockStore()
  })
    .then(() => {
      console.log("PACKED")
      res.send({
        "status": 200,
        "output": output
      })
    })
    .catch((error) => {
      console.log(error)
      res.send({
        "status": 404,
        "error": error
      })
    })
}


app.post('/generate-car', async (req, res) => {
  if (fs.existsSync(CAR_PATH)) {
    res.send({
      "status": 404,
      "error": "CAR File already exists"
    })
  } else {
    generate_car(req, res)
  }
});

app.post('/upload-car', async (req, res) => {
  console.log("STARTING UPLOAD CAR")
  const client = new NFTStorage({ token: req.body.token })

  if (fs.existsSync(CAR_PATH)) {
    let cid = null

    let car = await CarReader.fromIterable(fs.createReadStream(CAR_PATH))
    console.log("UPLOADING", file)
    cid = await client.storeCar(car)
    console.log("UPLOADED", file, cid)
    res.send({
      "status": 200,
      "cid": cid
    })
  } else {
    res.send({
      "status": 404,
      "error": "File not found, try to generate car before."
    })
  }
});

app.post('/get-cid', async (req, res) => {
  console.log("CONVERTING TO V1")
  const files = req.body.files
  files.forEach(file => {
    // GENERATE CID V1
    file["cid"] = `bafkr${CID.parse(file["base58"]).toV1().toString().substring(5)}`
    delete file["base58"]
  })
  console.log("CONVERTED TO V1")

  res.send({
    "status": 200,
    "files": files
  })
});

app.get('/is-alive', async (_, res) => {
  res.send({
    "status": 200,
    "is_active": true
  })
});

app.listen(CAR_API_PORT, API_IP);
