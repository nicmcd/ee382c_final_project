

namespace Synfull_App {

	MsgTime::MsgTime(InjectReqMsg msg, u64 time) : _msg(msg), _time(time) {

	}
	MsgTime::~MsgTime() {}

	InjectReqMsg MsgTime::getMsg() {
		return _msg;
	}

	u64 MsgTime::getTime() {
		return _time;
	}
}