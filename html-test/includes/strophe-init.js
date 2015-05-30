connection.connect(chatJID, chatPasswd, onConnect);
                        
function onConnect(status) {
  if (status == Strophe.Status.CONNECTING) {
    console.log('Strophe is connecting.');
  } else if (status == Strophe.Status.CONNFAIL) {
    console.log('Strophe failed to connect.');
  } else if (status == Strophe.Status.DISCONNECTING) {
    console.log('Strophe is disconnecting.');
  } else if (status == Strophe.Status.DISCONNECTED) {
    console.log('Strophe is disconnected.');
  } else if (status == Strophe.Status.CONNECTED) {
    console.log('Strophe is connected.');
    connection.addHandler(onMessage, null, 'message', null, null,  null); 
    connection.send($pres().tree());
    
    // TODO: figure out why using admin@admin account won't work...This part requires more thinking...
    // using the other account won't allow me to receive onMessage either...
    // Instead of using defaultMucNickName, we can try with a random string, 
    // since from the point of view of a user, the nickname is always overwritten
    
    if (defaultMucRoom !== undefined && defaultMucRoom != '' && defaultMucNickName !== undefined && defaultMucNickName != '') {
      connection.muc.join(defaultMucRoom, defaultMucNickName, onMessage, onPresence, onRoster);
    }
    
    if (defaultMucRoom2 !== undefined && defaultMucRoom2 != '' && defaultMucNickName2 !== undefined && defaultMucNickName2 != '') {
      connection.muc.join(defaultMucRoom2, defaultMucNickName2, onMessage, onPresence, onRoster);
    }
  }
}

function onMessage(message) {
  //console.log(message);
}

function onPresence(presence) {
  //console.log(presence);
}

function onRoster(roster) {
  //console.log(roster);
}

window.onbeforeunload = function () {
  console.log("Page unload");
  connection.options.sync = true; 
  connection.flush();
  connection.disconnect();
};