const ws_scheme = window.location.protocol == 'https:' ? 'wss' : 'ws';
//const ws_scheme = "ws";

let signallingChannel

signallingChannel = new WebSocket(
    ws_scheme
    + '://'
    + window.location.host
    + '/ws/chat_interfon3/'
    //+ roomName 
    //+ "/"
    //+ name
    //+ '/'
);


let peerConnection

/*
function handleSignallingData(data) {
    console.log(data)
    switch (data.case) {

        case "test_message":
            console.log("test message",data.message)
            break

        case "offer":

            //peerConnection.setRemoteDescription(new RTCSessionDescription(data.message));
            //const answer = await peerConnection.createAnswer();
            //await peerConnection.setLocalDescription(answer);        
            //alert(answer)

            break

        case "answer":
            //peerConnection.setRemoteDescription(data.message)
            break

        case "candidate":
            //peerConnection.addIceCandidate(data.message)
    }
}
*/

/*
signallingChannel.onmessage = (event) => {
    console.log("event.data:  ",event.data)
    handleSignallingData(JSON.parse(event.data))
}
*/


signallingChannel.onmessage = async (event) => {

    //console.log("event.data:  ",event.data)
    //await handleSignallingData(JSON.parse(event.data))

    //console.log(event)
    console.log(event.data)
    //console.log(event.data.case)

    data = JSON.parse(event.data);
    switch (data.case) {

        case "test_message":
            console.log("test message",data.message)
            break

        case "offer":

            peerConnection.setRemoteDescription(new RTCSessionDescription(data.message));
            answer = await peerConnection.createAnswer();
            await peerConnection.setLocalDescription(answer);        
            await sendData("answer",answer);

            break

        case "answer":
            //console.log(data.message)
            //peerConnection.setRemoteDescription(data.message)

            const remoteDesc = new RTCSessionDescription(data.message);
            await peerConnection.setRemoteDescription(remoteDesc);

            break

        case "candidate":
            console.log("candidate!: ",data.message)
            //peerConnection.addIceCandidate(data.message)

            try {
                await peerConnection.addIceCandidate(data.message);
            } catch (e) {
                console.error('Error adding received ice candidate', e);
            }

            break;
    }


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

    offer = await peerConnection.createOffer();
    await peerConnection.setLocalDescription(offer);

    await sendData("offer",offer);
}

const stoptButton = document.getElementById('stopButton');
stopButton.onclick = async () => {
    await sendData("reset","");
}    


const configuration = {
    iceServers: [
        {
            urls: [
                "stun:stun.l.google.com:19302",
                "stun:stun1.l.google.com:19302",
                "stun:stun2.l.google.com:19302"
            ]
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

    peerConnection = new RTCPeerConnection(configuration);

    localStream = await navigator.mediaDevices.getUserMedia({video:true, audio:true})
    remoteStream = new MediaStream()
    document.getElementById('localVideo').srcObject = localStream
    document.getElementById('remoteVideo').srcObject = remoteStream

    localStream.getTracks().forEach((track) => {
        peerConnection.addTrack(track, localStream);
    });

    peerConnection.ontrack = (event) => {
        event.streams[0].getTracks().forEach((track) => {
        remoteStream.addTrack(track);
        });
    };






    // Monitor ICE connection state changes ?
    peerConnection.oniceconnectionstatechange = () => {
        console.log('ICE connection state changed:', peerConnection.iceConnectionState);
    };

    // Monitor ICE candidate errors ?
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
            /*
            chatSocket.send(JSON.stringify({
                'prop': 'candidate',
                'message': event.candidate,
                'recipient_name': destination.value
            }));  
            */

            sendData("candidate",event.candidate);

        } else {
            // If all candidates have been sent, this event will be triggered with a null candidate
            console.log("ICE candidate gathering complete.");
        }
    };



}

init();