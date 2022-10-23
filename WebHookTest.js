/**
 * This example demonstrates setting up a webook, and receiving
 * updates in your express app
 */
/* eslint-disable no-console */

// const TOKEN = process.env.TELEGRAM_TOKEN || 'YOUR_TELEGRAM_BOT_TOKEN';
const TOKEN = "5572953233:AAFQFs4Qf4bNCICOBaa7Ft6m2VBe6Vn2F9I";
const url = "https://34aa-190-201-204-182.ngrok.io";
const port = 8080;

const TelegramBot = require("/Users/xavierorejarena/Desktop/Marioneta/node_modules/node-telegram-bot-api");
const express = require("/Users/xavierorejarena/Desktop/Marioneta/node_modules/express");

// No need to pass any parameters as we will handle the updates with Express
const bot = new TelegramBot(TOKEN);

// This informs the Telegram servers of the new webhook.
bot.setWebHook(`${url}/bot${TOKEN}`);

const app = express();

// parse the updates to JSON
app.use(express.json());

// We are receiving updates at the route below!
app.post(`/bot${TOKEN}`, (req, res) => {
  bot.processUpdate(req.body);
  res.sendStatus(200);
});

// Start Express Server
app.listen(port, () => {
  console.log(`Express server is listening on ${port}`);
});

// Just to ping!
bot.on("message", (msg) => {
  bot.sendMessage(msg.chat.id, "I am alive!");
});
