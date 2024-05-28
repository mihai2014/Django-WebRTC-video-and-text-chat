
let peerConnection = new RTCPeerConnection()
let localStream;
let remoteStream;

let init = async () => {  console.log("start")
    localStream = await navigator.mediaDevices.getUserMedia({video:true, audio:true})
    remoteStream = new MediaStream()
    document.getElementById('user-1').srcObject = localStream
    document.getElementById('user-2').srcObject = remoteStream

    localStream.getTracks().forEach((track) => {
        peerConnection.addTrack(track, localStream);
    });

    peerConnection.ontrack = (event) => {
        event.streams[0].getTracks().forEach((track) => {
        remoteStream.addTrack(track);
        });
    };
}


let createOffer = async () => {  console.log("da");


    peerConnection.onicecandidate = async (event) => {
        //Event that fires off when a new offer ICE candidate is created
        if(event.candidate){
            console.log(event.candidate)
            //console.log("Creating offer...:",JSON.stringify(peerConnection.localDescription))
            document.getElementById('offer-sdp').value = JSON.stringify(peerConnection.localDescription)

            //offer_data = JSON.stringify(peerConnection.localDescription);

            // Send offer_data over WebSocket
            //console.log("ws: ...",ws);
            //ws.send(offer_data);
            console.log("------------")
            
            //ws.send(JSON.stringify({
            //    'message': 'offer',
            //    'recipient_name': 'john'
            //}));
            
        }
    };

    const offer = await peerConnection.createOffer();
    await peerConnection.setLocalDescription(offer);
  
}

let createAnswer = async () => {

    let offer = JSON.parse(document.getElementById('offer-sdp').value)

    peerConnection.onicecandidate = async (event) => {
        //Event that fires off when a new answer ICE candidate is created
        if(event.candidate){
            //console.log('Adding answer candidate...:', event.candidate)
            document.getElementById('answer-sdp').value = JSON.stringify(peerConnection.localDescription)

            answer_data = JSON.stringify(peerConnection.localDescription);

        }
    };

    await peerConnection.setRemoteDescription(offer);

    let answer = await peerConnection.createAnswer();
    await peerConnection.setLocalDescription(answer); 
}

let addAnswer = async () => {
    console.log('Add answer triggerd')
    let answer = JSON.parse(document.getElementById('answer-sdp').value)
    console.log('answer:', answer)
    if (!peerConnection.currentRemoteDescription){
        console.log("conn set")
        peerConnection.setRemoteDescription(answer);
    }
}


init()

document.getElementById('create-offer').addEventListener('click', createOffer)
document.getElementById('create-answer').addEventListener('click', createAnswer)
document.getElementById('add-answer').addEventListener('click', addAnswer)
