from flask import Flask
import google.generativeai as genai

app = Flask(__name__)

genai.configure