let loc = window.location
let wsStart = 'ws://'

if(loc.protocol == 'https'){
    wsStart = 'wss://'
}
let endPoint = wsStart + loc.host + loc.pathname

var socket = new WebSocket(endPoint)

socket.onopen = async function(e){
    console.log('open', e)
}

socket.onmessage = async function(e){
    console.log('message', e)
}

socket.onerror = async function(e){
    console.log('error', e)
}

socket.onclose = async function(e){
    console.log('close', e)
}