import africastalking

africastalking.initialize("sandbox", "atsk_786188fd2f5fd391d7f50dd7cb5b442457dc676815fd45779242dc41e822a02d8567698f")
sms = africastalking.SMS

try:
    response = sms.send("Test message", ["+254799604144"])
    print("Message sent:", response)
except Exception as e:
    print("Failed to send message:", str(e))
