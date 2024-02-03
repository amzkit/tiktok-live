
const qs = require('qs');
const { WebcastPushConnection } = require('tiktok-live-connector');
// Username of someone who is currently live
let tiktokUsername = "prw.xx";

const spawn = require("child_process").spawn
//const pythonProcess = spawn('python', ["gTTS.py", "เชื่อมต่อแล้ว"])

// Create a new wrapper object and pass the username
let tiktokLiveConnection = new WebcastPushConnection(tiktokUsername);

// Connect to the chat (await can be used as well)
tiktokLiveConnection.connect().then(state => {
    console.info(`[${new Date().toLocaleTimeString()}] Connected to roomId ${state.roomId}`);
    notify(tiktokUsername, "เชื่อมต่อแล้ว");

}).catch(err => {
    console.error('Failed to connect', err);
})

// Define the events that you want to handle
// In this case we listen to chat messages (comments)
tiktokLiveConnection.on('chat', data => {
    console.log(`[${new Date().toLocaleTimeString()}] ${data.uniqueId} : ${data.comment}`);
    notify(data.uniqueId, data.comment);

})

tiktokLiveConnection.on('streamEnd', (actionId) => {
    if (actionId === 3) {
        console.log('Stream ended by user');
    }
    if (actionId === 4) {
        console.log('Stream ended by platform moderator (ban)');
    }
    notify(data.uniqueId, "ไลฟ์หลุดแล้ว");

})

// And here we receive gifts sent to the streamer
tiktokLiveConnection.on('gift', data => {
    console.log(`${data.uniqueId} (userId:${data.userId}) sends ${data.giftId}`);
})

const url_line_notification = "https://notify-api.line.me/api/notify";
const TOKEN = "PNTRtn2tZDnz6zI3mVRC4o7xthxogTVwDmo21HI2r07";
const axios  = require('axios')

function notify(userId, comment){
    //console.log(msg)

    let message = '['+userId+'] '+comment
    //message = qs.stringify(message)
    //console.log(message, userId, comment)
    axios.post(
        url_line_notification,
        qs.stringify({
            message: message
        }),
        {
            headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization' : 'Bearer ' + TOKEN
            }
        },
        ).then(function (response) {
            //console.log('Notify Successfully : ',response.data);
            //Logic process save notification logs
            const pythonProcess = spawn('python', ["gTTS.py", comment])
            return response;
        })
        .catch(function (error) {
            console.error('Notification Error : ',error.toJSON());
        });
        
}