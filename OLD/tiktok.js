
const qs = require('qs');
const { WebcastPushConnection } = require('tiktok-live-connector');
// Username of someone who is currently live
let tiktokUsername = "janua_official";
let create_time = null
let time_duration = null
let connected = false

let remaining_seconds = 0

const url_line_notification = "https://notify-api.line.me/api/notify";
const TOKEN = "CPF3M1CLAuEGUxHP2S5WnmjdeeDiZtcwyLxhb5stCsW";
const axios  = require('axios')

const spawn = require("child_process").spawn
//const pythonProcess = spawn('python', ["gTTS.py", "เชื่อมต่อแล้ว"])

// Create a new wrapper object and pass the username
let tiktokLiveConnection = new WebcastPushConnection(tiktokUsername);

// Connect to the chat (await can be used as well)
tiktokLiveConnection.connect().then(state => {
    create_time = state.roomInfo.create_time
    time_duration = duration(state.roomInfo.create_time)
    create_time = new Date(create_time * 1000).toLocaleTimeString('th-TH', {timeZone: "Asia/Bangkok", hour12: false})
    console.info(`[${new Date().toLocaleTimeString()}] ${tiktokUsername} connected | started at ${create_time} (${time_duration})`);

    connected = true

    let create_time_tmp = new Date(state.roomInfo.create_time * 1000)
    var time_now = new Date()

    let diff = (time_now - create_time_tmp) / 1000
    remaining_seconds = parseInt(diff) % 14400

    // 15 mins = 900 seconds
    setTimeout(function(){
        console.info(`[${new Date().toLocaleTimeString()}] ${tiktokUsername} remain 15 mins`);
    }, (14400-remaining_seconds-900)*1000)

    // 3 mins = 180 seconds
    setTimeout(function(){
        console.info(`[${new Date().toLocaleTimeString()}] ${tiktokUsername} remain 3 mins`);
    }, (14400-remaining_seconds-180)*1000)

    // 0 mins = 0 seconds
    setTimeout(function(){
        console.info(`[${new Date().toLocaleTimeString()}] ${tiktokUsername} is about to end`);
    }, (14400-remaining_seconds)*1000)
    
    //console.info(state);
    notify(tiktokUsername, `connected | started at ${create_time} (${time_duration})`);

}).catch(err => {
    console.error('Failed to connect', err);
})

// Define the events that you want to handle
// In this case we listen to chat messages (comments)
tiktokLiveConnection.on('chat', data => {
    console.log(`[${new Date().toLocaleTimeString()}] ${data.uniqueId} : ${data.comment}`);
    let message = data.comment

    if(message.startsWith("@")){
        let space_position = -1
        space_position = message.search(" ")
        if(space_position > 0)
            message = message.substr(space_position)
    }

    const pythonProcess = spawn('python', ["gTTS.py", message])
    notify(data.uniqueId, message);

})

// And here we receive gifts sent to the streamer
tiktokLiveConnection.on('gift', data => {
    console.log(`${data.uniqueId} (userId:${data.userId}) sends ${data.giftId}`);
})

function notify(userId, comment){
    //console.log(msg)

    let message = '['+userId+'] '+comment
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
            return response;
        })
        .catch(function (error) {
            console.error('Notification Error : ',error.toJSON());
        });
        
}

function duration(create_time){

    let create_time_tmp = new Date(create_time * 1000)
    let now = new Date()

    let diff = (now - create_time_tmp) / 1000
    let time_tmp = new Date(null)
    time_tmp.setSeconds(diff)
    console.log(time_tmp)
    time_tmp = time_tmp.toISOString().substr(11,8)

    return time_tmp
}