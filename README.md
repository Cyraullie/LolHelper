# LoL Helper - Discord Bot

A Discord bot that notifies users about upcoming League of Legends Clash events using the Riot Games API.

## Features
- Automatic Clash event detection
- Discord embed notifications
- Role ping system
- Anti-duplicate notifications
- Scheduled API polling (30 minutes)

## API Used
This project uses the Riot Games API:
- /lol/clash/v1/tournaments

## Technical Details
- Polling interval: 30 minutes
- Caching system to respect rate limits
- UTC timestamp conversion
- Persistent storage for notified events

## Purpose
To help Discord communities stay informed about upcoming Clash tournaments in League of Legends.

## Disclaimer
This project is not affiliated with Riot Games.