from flask import Blueprint, render_template, request, flash, redirect, url_for
import random
from flask_mailman import Mail, EmailMessage
from .models import User