/*
 * Copyright 2016 Hewlett Packard Enterprise Development LP
 *
 * Licensed under the Apache License, Version 2.0 (the 'License');
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *  http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#include "application/synfull_app/SynfullTerminal.h"

#include <cassert>
#include <cstring>

#include "event/Simulator.h"
#include "types/Message.h"
#include "types/Packet.h"
#include "types/Flit.h"
#include "application/synfull_app/Application.h"
#include "application/synfull_app/MsgTime.h"
namespace Synfull_App {

SynfullTerminal::SynfullTerminal(
    const std::string& _name, const Component* _parent, u32 _id,
    const std::vector<u32>& _address, ::Application* _app,
    Json::Value _settings)
    : ::Terminal(_name, _parent, _id, _address, _app),
      fsm_(eState::kWaiting) {
  latency_ = _settings["latency"].asUInt();
    maxPacketSize_  = 16;

}

SynfullTerminal::~SynfullTerminal() {
}

void SynfullTerminal::processEvent(void* _event, s32 _type) {
  // sendMemoryResponse();
}

void SynfullTerminal::handleMessage(Message* _message) {
  dbgprintf("received message");
  // log the message
  endTransaction(_message->getTransaction());
  Application* app = reinterpret_cast<Application*>(gSim->getApplication());
  app->getMessageLog()->logMessage(_message);
  MsgTime* data = reinterpret_cast<MsgTime*>(_message->getData());
  app->enqueueMessage(_message);
  // optional: add latency here
  //  startMemoryAccess();
}

void SynfullTerminal::sendSynfullPacket(InjectReqMsg* msg) {
  u32 messageLength = msg->packetSize;
  u32 numPackets = messageLength / maxPacketSize_;
  if ((messageLength % maxPacketSize_) > 0) {
    numPackets++;
  }
  MsgTime* msgtime = new MsgTime(msg, gSim->time());
  // create the message object
  Message* message = new Message(numPackets, msgtime);
  message->setTransaction(createTransaction());

  // create the packets
  u32 flitsLeft = messageLength;
  for (u32 p = 0; p < numPackets; p++) {
    u32 packetLength = flitsLeft > maxPacketSize_ ?
        maxPacketSize_ : flitsLeft;

    Packet* packet = new Packet(p, packetLength, message);
    message->setPacket(p, packet);

    // create flits
    for (u32 f = 0; f < packetLength; f++) {
      bool headFlit = f == 0;
      bool tailFlit = f == (packetLength - 1);
      Flit* flit = new Flit(f, headFlit, tailFlit, packet);
      packet->setFlit(f, flit);
    }
    flitsLeft -= packetLength;
  }

  // send the message
  u32 msgId = sendMessage(message, msg->dest);
}

void SynfullTerminal::messageEnteredInterface(Message* _message) {
}

void SynfullTerminal::messageExitedNetwork(Message* _message) {
  // any override of this function must call the base class's function
  ::Terminal::messageExitedNetwork(_message);
}

void SynfullTerminal::addLatency() {
  addEvent(gSim->futureCycle(latency_), 0, nullptr, 0);
  fsm_ = eState::kAccessing;
}



}  // namespace Synfull_App
