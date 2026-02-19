# To ensure maximum self-recoverability, safemode.py is set to do a 
# hard reset of the microcontroller if entered.
# there are reasons you may *not* want to do this. Be particulary
# cautious of inadvertently spamming your IO feed if you get caught in a boot loop.
import microcontroller

microcontroller.reset()