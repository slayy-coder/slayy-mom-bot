# Slayy Mom Discord Bot

A supportive, LGBTQIA+ inclusive Discord bot that acts as a warm, caring "mom" figure for your server community.

## Features

### User Setup
- Set preferred pronouns with `!pronouns`
- Manage personal triggers with `!trigger add/remove/list`
- Track important dates with `!birthday` and `!milestone`
- Customize your experience with the bot

### Affirmations & Emotional Support
- Get daily affirmations automatically or on-demand with `!affirmation`
- Receive comforting messages with `!comfort`
- Create a private vent thread with `!vent`
- Celebrate achievements with `!celebrate`

### Inclusive & Safe Features
- Basic moderation tools: `!warn`, `!mute`
- LGBTQIA+ resources directory with `!resources`
- Pride-themed messages with `!pride`
- Trigger warnings for sensitive content with `!tw`

### Privacy Features
- Delete all your stored data with `!forgetme`
- Minimal data collection policy

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- A Discord account and a server where you have admin permissions
- Discord Developer Portal access

### Step 1: Create a Discord Bot
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Navigate to the "Bot" tab and click "Add Bot"
4. Under the "Privileged Gateway Intents" section, enable:
   - Presence Intent
   - Server Members Intent
   - Message Content Intent
5. Copy your bot token (keep this secret!)

### Step 2: Install the Bot
1. Clone this repository or download the files
2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory with your bot token:
   ```
   DISCORD_TOKEN=your_token_here
   COMMAND_PREFIX=!  # Optional, defaults to !
   AFFIRMATION_CHANNEL_ID=channel_id_here  # Optional, for daily affirmations
   ```

### Step 3: Invite the Bot to Your Server
1. In the Discord Developer Portal, go to your application
2. Navigate to the "OAuth2" tab and then "URL Generator"
3. Select the following scopes:
   - `bot`
   - `applications.commands`
4. Select the following bot permissions:
   - Send Messages
   - Embed Links
   - Attach Files
   - Read Message History
   - Add Reactions
   - Use External Emojis
   - Manage Messages (for moderation)
   - Manage Threads (for vent feature)
   - Moderate Members (for timeout feature)
5. Copy the generated URL and open it in your browser
6. Select your server and authorize the bot

### Step 4: Run the Bot
```
python main.py
```

## Command Reference

### User Setup Commands
- `!pronouns [your/pronouns]` - Set or view your preferred pronouns
- `!trigger add [word]` - Add a word to your trigger list
- `!trigger remove [word]` - Remove a word from your trigger list
- `!trigger list` - View your trigger list (sent via DM for privacy)
- `!birthday [DD-MM-YYYY]` - Set or view your birthday
- `!milestone [DD-MM-YYYY] [description]` - Add a personal milestone to celebrate

### Support Commands
- `!affirmation` - Get a positive affirmation
- `!comfort` - Receive comforting words
- `!vent [optional topic]` - Create a private thread to vent
- `!celebrate [achievement]` - Celebrate an achievement

### Inclusive Features
- `!resources [optional category]` - Get LGBTQIA+ resources
- `!pride [optional flag]` - Send a pride-themed message
- `!tw [topic] [message]` - Add a trigger warning to a message

### Moderation Commands
- `!warn [user] [reason]` - Warn a user (requires Manage Messages permission)
- `!mute [user] [duration in minutes] [reason]` - Timeout a user (requires Moderate Members permission)

### Other Commands
- `!help [optional command]` - View help information
- `!forgetme` - Delete all your stored data

## Customization

### Adding Custom Affirmations
Edit the `data/affirmations.json` file to add your own affirmations.

### Adding Custom Resources
Edit the `data/resources.json` file to add your own LGBTQIA+ resources.

## Privacy & Data

Slayy Mom Bot stores minimal user data:
- User preferences (pronouns, triggers, etc.)
- Important dates (birthdays, milestones)

All data is stored locally in JSON files and is not shared with third parties. Users can delete their data at any time using the `!forgetme` command.

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues for new features or bug fixes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.