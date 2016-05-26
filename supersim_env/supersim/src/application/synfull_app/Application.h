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
#ifndef APPLICATION_SYNFULL_APP_APPLICATION_H_
#define APPLICATION_SYNFULL_APP_APPLICATION_H_

#include <json/json.h>
#include <prim/prim.h>

#include <string>
#include <queue>

#include "event/Component.h"
#include "application/Application.h"
#include "types/Message.h"

class MetadataHandler;

namespace Synfull_App {

class Application : public ::Application {
 public:
  Application(const std::string& _name, const Component* _parent,
              MetadataHandler* _metadataHandler, Json::Value _settings);
  ~Application();
  u32 numVcs() const;
  u32 bytesPerFlit() const;
  u32 headerOverhead() const;
  u32 maxPacketSize() const;
  void processEvent(void* _event, s32 _type) override;
  f64 percentComplete() const override;
  void enqueueMessage(Message* message);


 private:
  u32 numVcs_;
  u32 bytesPerFlit_;
  u32 headerOverhead_;
  u32 maxPacketSize_;
  std::queue<Message*> finished_;
};

}  // namespace Synfull_App

#endif  // APPLICATION_SYNFULL_APP_APPLICATION_H_
