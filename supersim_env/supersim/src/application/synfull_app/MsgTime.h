
#include <prim/prim.h>
#include "../../Synfull/src/netstream/messages.h"



namespace Synfull_App {

	class MsgTime
	{
	public:
		MsgTime();
		~MsgTime();
		InjectReqMsg getMsg();
		u64 getTime();

	private:
		InjectReqMsg _msg;
		u64 _time;

	};

}