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
#ifndef APPLICATION_SYNFULL_APP_SYNFULLTERMINAL_H_
#define APPLICATION_SYNFULL_APP_SYNFULLTERMINAL_H_

#include <json/json.h>
#include <prim/prim.h>

#include <queue>
#include <string>
#include <vector>

#include "event/Component.h"
#include "application/Terminal.h"
#include "Synfull/src/netstream/messages.h"

class Application;

namespace Synfull_App {

class SynfullTerminal : public Terminal {
 public:
  SynfullTerminal(const std::string& _name, const Component* _parent,
                 u32 _id, const std::vector<u32>& _address,
                 ::Application* _app, Json::Value _settings);
  ~SynfullTerminal();
  void processEvent(void* _event, s32 _type) override;
  void handleMessage(Message* _message) override;
  void messageEnteredInterface(Message* _message) override;
  void messageExitedNetwork(Message* _message) override;
  void sendSynfullPacket(InjectReqMsg* msg);

 private:
  enum class eState {kWaiting, kAccessing};

  void addLatency();

  u32 latency_;
  u32 minMessageSize_;
  u32 maxMessageSize_;
  u32 maxPacketSize_;
  std::queue<Message*> messages_;
  eState fsm_;
};

}  // namespace Synfull_App

#endif  // APPLICATION_SYNFULL_APP_SYNFULLTERMINAL_H_
