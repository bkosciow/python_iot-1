#IOT:1

My custom protocol for communication between devices at home. 
It uses UPD and broadcast. 
Messages are json strings.

## Message body:

    {
        "protocol": "iot:1",
        "node": "Rpi-lcd-1",
        "chip_id": "RpiB",
        "event": "lcd.content",
        "parameters: [
            "content": "-(=^.^)"
        ],
        "response": '',
        "targets": [
            "nodemcu-lcd-40x4"
        ]
    }
    
- protocol: defines name, currently iot:1
- node: friendly node name like light-room-big or screen-one-kitchen
- chip_id: a unique device id
- event: event name like light.on or display
- parameters: array of parameters. like rows to display
- response: used when responding to request, ie returning toilet state
- targets: message targets node with this names. special keyword ALL for all nodes in network

## set node name or/and chip_id

Message.chip_id = 'miau'
Message.node_name = 'miau_too'

### Message()

Create new instance. It is automatically filled with chip_id and node_name if not set 

### Message(string_message)

Creates message and fills with received data
input = """{"protocol": "iot:1", "node": "node_name", "chip_id": "aaa", "event": "channel.on", "parameters": {"channel": 0}, "response": "", "targets": ["node-north"]}"""
msg = factory.MessageFactory.create(input)
        
## functions

### set(dictionary)

msg = message.Message()
msg.set({
    'event': 'event.test',
    'parameters': {
        'is_x': '1'
    }
})

Fills message with params.

### send message

s.sendto(bytes(msg), address)
     
## encders

- base64

Message.encoder = B64()

Message.add_decoder(B64())

     