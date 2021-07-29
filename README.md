# blob_ball
Slime Soccer type game

**v0.5.3b**

**Features:**
* Casual Matches!
* 31 of the exact same blob!
* 4 unique blobs!
* Physics system that works 99.6% of the time!
* High Octane Matches!
* Lots of advanced tech!
* A nifty UI that displays the things you need to know at a glance!
* Rebindable keys for those who don't like the default controls!
* A beautiful gameplay background, courtesy of Ellexium! Check out his YT channel: https://www.youtube.com/channel/UCNYthNCVDDovhbhTXVzMM4A
* Adjustable gameplay rules for more varied games!
* A glossary can be found here: https://docs.google.com/document/d/1pBm3NZczNl7L7mupscWfpWABMAau6Hw6TZptCThz_rA/edit?usp=sharing

**Controls:**

*P1:*
* Movement: WASD
* Use Ability/Select on Menu: 1
* Kick Ball/Deselect on Menu: 2
* Block Ball: 3
* Use Stat Boost: 4

*P2:*
* Movement: Arrow Keys
* Use Ability/Select on Menu: N
* Kick Ball/Deselect on Menu: M
* Block Ball: Comma
* Use Stat Boost: Period



*Other:*
* Quit Game: ESC


**Changelog**
Made huge changes!
New Stuff:
Rock Blob Added
Slow and Sturdy base stats, but has slow defensive options
Ability: Spire! After a short delay, a spire appears below the ball, which pops the ball up and damages opposing blobs if they get too close
New Game Rules
Danger Zone Bonus Toggle: Determines whether or not the danger zone gives a damage bonus
NRG Charge Rate: Determines how quick the base charge rate of the NRG bar is
Settings and Key Rebinds
Settings screen has been added to the game!
Toggle HD background (courtesy of Ellexium), and use the old SD background instead
Toggle HD Blobs (currently unused)
Rebind keys to your liking! The keybinds will be saved on the disk in controls.txt next time you open the game!
You cannot rebind keys to something that is already use (for example, you can't bind kick and block to the same button)
Also, there is a cool gear icon I drew for the Character Select Screen :)

Aesthetics:
New Gameplay Background, courtesy of Ellexium
Added particle effects for Fireball, Snowball and Geyser
Block Box visual has been updated
Horizontal size increased to better match the actual block box
Block Box now fades out
Player 1 and Player 2 have been swapped
In-game UI has been changed
NRG bar has been made shorter and wider
NRG bar has larger color contrasts between ability ready and not enough NRG
Kick/Block/Boost/HP/Unused icons have been upscaled
Text upscaled to match

Game Balance:
Reverted the Dribble Glitch "fix"
Fixed Kicking Mechanics
Abilities will be forcefully deactivated upon scoring
Buffed Fire Blob
Block Cooldown Rate Buffed: 3 stars --> 4 stars
Buffed Water Blob
Minimum geyser power buffed: 0.5 --> 0.8
Reworked Ice Blob
Top Speed Reduced (5 stars --> 4 stars) (Improves control and allows for more consistent wavebounces)
Snowball buffed (0.98x --> 0.975x) (Snowball now slows horizontal momentum slightly more every frame)
Reworked Base Mechanics to Rework Boost Kicking and Boosts
All Blob's health have been doubled (4, 5, 6, 7, 8 HP --> 8, 10, 12, 14, 16 HP)
Base Kick damage has been increased (1 DMG --> 2 DMG)
Boost Kick and Danger Zone Bonus stay the same (1 DMG --> 1 DMG)
Boost Top Speed Buffed (1 star --> 3 stars)
Boost Traction/Friction Buffed (1 star --> 5 stars)

Behind the Scenes:
Updated the ball to work with the particle system
Improved code organization
Updated the way graphics are handled. Game should look about the same for all screens
Fixed frame rate issues, game should now run at 60 FPS consistently.
** Game now records key information from games in blob_ball_results.txt**
Records the ruleset used
Records stats on each blob
Records stats on the ball
blob.type renamed to blob.species
ball.type renamed to ball.species
