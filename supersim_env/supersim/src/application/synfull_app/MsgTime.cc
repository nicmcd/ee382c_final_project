#ifndef MSG_TIME_CC
#define MSG_TIME_CC

#include "application/synfull_app/MsgTime.h"

namespace Synfull_App {

	MsgTime::MsgTime(InjectReqMsg* msg, u64 time) {
		_msg = msg;
		_time = time;
	}
	MsgTime::~MsgTime() {}

	InjectReqMsg* MsgTime::getMsg() {
		return _msg;
	}

	u64 MsgTime::getTime() {
		return _time;
	}

	void MsgTime::setTime(u32 new_val) {
		_time = new_val;
	}
}

#endif