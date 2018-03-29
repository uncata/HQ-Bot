# HQ-Bot
Bot that can guess answers for the the live trivia game, HQ

## Prerequisites
HQ-Bot needs the following python3 modules:
```
bs4
PIL
lxml
pytesseract
re
requests
time
```

## Usage
Add the following line to the end of bot.py:
```python
guessAnswer('examplePath/example.png')
```

Image:
![Question 1](/images/Q1.png)

Console Output:
```
['Trees often grow from what?', 'AstroTu rf', 'Seeds', 'Peanut butter']
answer is probably Seeds
--- 3.190742254257202 seconds ---
```

## Note
HQ-Bot is ~90% accurate since it uses google search to predict the best answer. Accuracy may vary with more questions, as HQ-Bot was only tested on 21 questions. 
## LICENSE

[MIT License](LICENSE)
