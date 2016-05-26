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
#include "application/synfull_app/Application.h"

#include <cassert>

#include <vector>
#include <queue>
#include "application/synfull_app/SynfullTerminal.h"
#include "event/Simulator.h"
#include "network/Network.h"

// TODO(rprabala): make this the correct path
#include "../../SynFull/NetworkInterface.h"

#define ISPOW2INT(X) (((X) != 0) && !((X) & ((X) - 1)))  /*glibc trick*/
#define ISPOW2(X) (ISPOW2INT(X) == 0 ? false : true)

namespace Synfull_App {

Application::Application(const std::string& _name, const Component* _parent,
                         MetadataHandler* _metadataHandler,
                         Json::Value _settings)
    : ::Application(_name, _parent, _metadataHandler, _settings) {
  numVcs_ = gSim->getNetwork()->numVcs();
  assert(numVcs_ > 0);

  // check the memory system setup

  bytesPerFlit_ = _settings["bytes_per_flit"].asUInt();
  assert(bytesPerFlit_ > 0);
  headerOverhead_ = _settings["header_overhead"].asUInt();
  maxPacketSize_ = _settings["max_packet_size"].asUInt();

  // create terminals
  for (u32 t = 0; t < numTerminals(); t++) {
    std::vector<u32> address;
    gSim->getNetwork()->translateIdToAddress(t, &address);
    std::string idStr = std::to_string(t);
    std::string tname = "SynfullTerminal_" + idStr;
    SynfullTerminal* terminal = new SynfullTerminal(
        tname, this, t, address, this, _settings["synfull_terminal"]);
    setTerminal(t, terminal);
  }
  finished_ = new std::queue<Message*>();
  // this application always wants monitor
  addEvent(0, 0, nullptr, 0);
  gSim->startMonitoring();
}

Application::~Application() {}


u32 Application::numVcs() const {
  return numVcs_;
}

u32 Application::bytesPerFlit() const {
  return bytesPerFlit_;
}

u32 Application::headerOverhead() const {
  return headerOverhead_;
}

u32 Application::maxPacketSize() const {
  return maxPacketSize_;
}

f64 Application::percentComplete() const {
  return 0.5;
}

void Application::enqueueMessage(Message *message) {
  finished_.push(message);
}

Message* Application::dequeueMessage() {
  return finished_.pop();
}

u32 Application::remainingMessages() {
  return finished_.size();
}

void Application::processEvent(void* _event, s32 _type) {
  dbgprintf("synfull_app application starting\n");
  bool done = NetworkInterface::Step();
  if (!done)
    addEvent(gSim->FutureCycle(1), 0, nullptr, 0);
  else
    gSim->endMonitoring();
}

}  // namespace Synfull_App
