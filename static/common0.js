const chatArea = document.getElementById('chat-log');
const chatAllUsers = document.querySelector('#chat-allusers');
const chatDestination = document.querySelector('#chat-destination');
const selectedIdLi = document.querySelector('#selected-id-li');


const ws_scheme = window.location.protocol == 'https:' ? 'wss' : 'ws';
//const ws_scheme = "ws";

let signallingChannel

const room_name = "AAA"
const user_name = "username"



//console.log("{{user_name}}")


signallingChannel = new WebSocket(
    ws_scheme
    + '://'
    + window.location.host
    + '/ws/chat_interfon4/'
    + room_name 
    + "/"
    + user_name
    + '/'
);






document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.key === 'Enter') {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    /*
    chatSocket.send(JSON.stringify({
        'prop': "message",
        'message': message
    }));
    */
    sendData("chat_all",message);
    messageInputDom.value = '';
};



function createList(allusers,channel){
    const ul = document.querySelector('#userslist');

    ul.innerHTML = ""

    //console.log(allusers)
    users_list = JSON.parse(allusers["users"])
    console.log("lista:",users_list)

    /*
    display = ""
    for(var key in allusers) {
        display += allusers[key];
    }                    
    chatAllUsers.value = display;
    */


    for(var key in users_list) {
        //console.log(key)
        //channel = allusers[key];
        li = document.createElement('li');
        for (key2 in users_list[key]){
            //console.log(key,key2)
            username = users_list[key][key2]["user"]
            li.textContent = username;
            li.value = key;
            //li.value = "100"
        }    

        li.onclick = async function() {
            const clickedLi = this;
            console.log(clickedLi.value)

            selectedIdLi.value = clickedLi.value;
            chatDestination.value = clickedLi.textContent;

            //move this to Start ...
            selectedId = selectedIdLi.value;
            selectedUser = users_list[selectedId]
            //have only one key...
            for (key in selectedUser){
                console.log(key)
                channel = key
                //alert(channel)

                //await sendData("channel",channel);
            }
            

        }    

        li.addEventListener('mouseenter', function() {
            const clickedLi = this;
            // Change background color of the list item when mouse enters
            clickedLi.style.backgroundColor = 'lightgray';
        });

        // Add mouseleave event listener to revert color when mouse leaves
        li.addEventListener('mouseleave', function() {
            const clickedLi = this;
            // Revert background color of the list item when mouse leaves
            clickedLi.style.backgroundColor = ''; // Empty string to revert to default
        });

        ul.appendChild(li);
    }        


}



let peerConnection
let localStream

let isAudio = true
function muteAudio() {
    isAudio = !isAudio
    localStream.getAudioTracks()[0].enabled = isAudio
}

let isVideo = true
function muteVideo() {
    isVideo = !isVideo
    localStream.getVideoTracks()[0].enabled = isVideo
}


signallingChannel.onmessage = async (event) => {

    //console.log("1",event)
    //console.log("2",event.data)
    //console.log("3",event.data.case)

    console.log("event",event)
    eventData = JSON.parse(event.data);
    //console.log("event.data",eventData)

    if(eventData.test_message){
        console.log("test message",eventData.test_message)

    }else if(eventData.user_join){
        console.log("user join",eventData.user_join)

        // Display user join event
        chatArea.value += `${eventData.user_join.name} joined the chat\n`;
        // Scroll to bottom
        chatArea.scrollTop = chatArea.scrollHeight;          
     
    }else if(eventData.user_leave){
        console.log("user leave",eventData.user_leave)

        // Display user join event
        chatArea.value += `${eventData.user_leave.name} lived the chat\n`;
        // Scroll to bottom
        chatArea.scrollTop = chatArea.scrollHeight;              

    }else if(eventData.user_sendall){
        console.log("user sendall",eventData.user_sendall)

        allusers = eventData.user_sendall;
        //chatAllUsers.value = allusers;
        createList(allusers,signallingChannel);

    }else if(eventData.chat_all){
        console.log("chat_all",eventData.chat_all)

        // Display user join event
        chatArea.value += `${eventData.chat_all}\n`;
        // Scroll to bottom
        chatArea.scrollTop = chatArea.scrollHeight;          
        

    }else if(eventData.offer){
        console.log("offer",eventData.offer)

        peerConnection.setRemoteDescription(new RTCSessionDescription(eventData.offer));
        answer = await peerConnection.createAnswer();
        await peerConnection.setLocalDescription(answer);        
        await sendData("answer",answer);

    }else if(eventData.answer){
        console.log("answer",eventData.answer)

        const remoteDesc = new RTCSessionDescription(eventData.answer);
        await peerConnection.setRemoteDescription(remoteDesc);        

    }else if(eventData.candidate){
        console.log("candidate",eventData.candidate)

        try {
            await peerConnection.addIceCandidate(eventData.candidate);
        } catch (e) {
            console.error('Error adding received ice candidate', e);
        }        
    }

    /*
    switch (data.case) {   

        case "test_message":
            console.log("test message",data.message)
            break
    }        
    */

}



function test1(data){
    data = {
        case: "test_message",
        message : "message from sender"
    }
    signallingChannel.send(JSON.stringify(data))
}


function test2(data){
    data = {
        case: "test_message",
        message : "message from receiver"
    }
    signallingChannel.send(JSON.stringify(data))
}


async function sendData(prop,message) {

    //offer = await peerConnection.createOffer();
    //await peerConnection.setLocalDescription(offer);

    signallingChannel.send(JSON.stringify({
        'case': prop,
        'message': message
    }));

}


const startButton = document.getElementById('startButton');

// Start button click event handler
startButton.onclick = async () => {

    //set chosen destination call
    selectedId = selectedIdLi.value;
    if (selectedIdLi == ""){
        alert("No destination selected!")
        return;
    }
    selectedUser = users_list[selectedId]
    //have only one key...
    for (key in selectedUser){
        console.log(key)
        channel_dest = key
        //alert(channel_dest)
    }

    offer = await peerConnection.createOffer();
    await peerConnection.setLocalDescription(offer);

    data = {
        channel_dest : channel_dest,
        offer : offer
    }

    //await sendData("offer",offer);

    //adaugam si channel-destination peer ...
    await sendData("offer",data);
}

const stoptButton = document.getElementById('stopButton');
stopButton.onclick = async () => {

    //reset user identities (SENDER/RECEIVER)
    //await sendData("reset","");

    
    if (peerConnection) {
        // Close peer connection
        peerConnection.close();
        peerConnection = null;
        init();
    }    
    

}    


const configuration = {
    iceServers: [
        {
            urls: [
                "stun:stun.l.google.com:19302",
                "stun:stun1.l.google.com:19302",
                "stun:stun2.l.google.com:19302"
            ],


            //{'urls': 'turns:intercom.microsif.ro:3478', username: 'username1', credential: 'password1'}

            //{'urls': 'stun:freeturn.net:3478' }, 
            //{'urls': 'turns:freeturn.tel:3478', username: 'free', credential: 'free' },

            //{'urls': 'stun:freeturn.net:5349' }, 
            //{'urls': 'turns:freeturn.tel:5349', username: 'free', credential: 'free' },

            //{ urls: 'stun:freestun.net:5350' }, { urls: 'turns:freestun.tel:5350', username: 'free', credential: 'free' } 


        },

        //{'urls': 'turns:intercom.microsif.ro:3478', username: 'username1', credential: 'password1'},

        //{'urls': 'stun:freeturn.net:3478' }, 
        //{'urls': 'turns:freeturn.tel:3478', username: 'free', credential: 'free' },

        //{'urls': 'stun:freeturn.net:5349' }, 
        //{'urls': 'turns:freeturn.tel:5349', username: 'free', credential: 'free' },

        //{ urls: 'stun:freestun.net:5350' }, { urls: 'turns:freestun.tel:5350', username: 'free', credential: 'free' }                 

    ]
};

let init = async () => {

    /*
    signallingChannel = new WebSocket(
        ws_scheme
        + '://'
        + window.location.host
        + '/ws/chat_interfon4/'
        + room_name 
        + "/"
        + user_name
        + '/'
    );
    */

    //alert(user_name)

    peerConnection = new RTCPeerConnection(configuration);

    localStream = await navigator.mediaDevices.getUserMedia({
        video:{
            frameRate: 24,
            width: {
                min: 480, ideal: 720, max: 1280
            },
            aspectRatio: 1.33333
        }, 
        audio:true
    })
    remoteStream = new MediaStream()
    document.getElementById('local-video').srcObject = localStream
    document.getElementById('remote-video').srcObject = remoteStream

    localStream.getTracks().forEach((track) => {
        peerConnection.addTrack(track, localStream);
    });

    peerConnection.ontrack = (event) => {
        event.streams[0].getTracks().forEach((track) => {
        remoteStream.addTrack(track);
        });
    };

    // Monitor ICE connection state changes
    peerConnection.oniceconnectionstatechange = () => {
        console.log('ICE connection state changed:', peerConnection.iceConnectionState);

        if(peerConnection.iceConnectionState == "disconnected"){

            // Close peer connection
            peerConnection.close();
            peerConnection = null;
            init();            
            
        }


        if(peerConnection.iceConnectionState == "connected"){

            //reset user identities (SENDER/RECEIVER): dont t need them anymore
            //sendData("reset","");

        }

    };

    // Monitor ICE candidate errors
    peerConnection.onicecandidateerror = (error) => {
        console.error('ICE candidate error:', error);
    };







    // Listen for local ICE candidates on the local RTCPeerConnection
    peerConnection.onicecandidate = function(event) {
    
        if (event.candidate) {
            
            //console.log(local,"->",destination.value)

            //console.log("new ice candidate send",window.local,window.remote)
            console.log("ICE candidate: ",event.candidate);
            
            // Check if it's a STUN candidate
            if (event.candidate.type === 'host' || event.candidate.type === 'srflx') {
                console.log('STUN candidate:', event.candidate);
            }

            sendData("candidate",event.candidate);

        } else {
            // If all candidates have been sent, this event will be triggered with a null candidate
            console.log("ICE candidate gathering complete.");
        }
    };



}

init();



// function set(user_name){

//     signallingChannel = new WebSocket(
//         ws_scheme
//         + '://'
//         + window.location.host
//         + '/ws/chat_interfon4/'
//         + room_name 
//         + "/"
//         + user_name
//         + '/'
//     );
    
//     console.log("user_name")
//     console.log(signallingChannel)

//     init();
// }