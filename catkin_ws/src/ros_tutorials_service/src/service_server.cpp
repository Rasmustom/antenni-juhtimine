// ROS Default Header File
#include "ros/ros.h"	
// SrvTutorial Service File Header (Automatically created after build)
#include "ros_tutorials_service/SrvTutorial.h"
// The below process is performed when there is a service request
// The service request is declared as 'req', and the service response is declared as 'res'

#define PLUS 1 // Addition
#define MINUS 2 // Subtraction
#define MULTIPLICATION 3 // Multiplication
#define DIVISION 4 // Division

int g_operator = PLUS;

bool calculation(ros_tutorials_service::SrvTutorial::Request &req, ros_tutorials_service::SrvTutorial::Response &res) {

	//The operator will be selected according to the parameter value and calculate 'a' aand 'b',
	// which were received upon the service request.
	// The result is stored as the Response value.
	switch(g_operator) {
		case PLUS:
			res.result = req.a + req.b;
			break;
		case MINUS:
			res.result = req.a - req.b;
			break;
		case MULTIPLICATION:
			res.result = req.a * req.b;
			break;
		case DIVISION:
			if (req.b != 0) {
				res.result = req.a / req.b;
				break;
			}
			res.result = 0;
			break;
		default:
			res.result = req.a + req.b;
			break;
	}



	// The service name is 'ros_tutorial_srv' and it will call 'calculation' function
	// upon the service request.
	//res.result = req.a + req.b;
	// Displays 'a' and 'b' values used in the service request and
	// the 'result' value corresponding to the service response
	ROS_INFO("request: x=%ld, y=%ld", (long int)req.a, (long int)req.b);
	ROS_INFO("sending back response: %ld", (long int)res.result);
	return true;
}

int main(int argc, char **argv) { 			// Node Main Function
	ros::init(argc, argv, "service_server"); 	 // Initializes Node Name
	ros::NodeHandle nh; 	 // Node handle declaration
	nh.setParam("calculation_method", PLUS);
	// Declare service server 'ros_tutorials_service_server'
	// using the 'SrvTutorial' service file in the 'ros_tutorials_service' package.
	// The service name is 'ros_tutorial_srv' and it will call 'calculation' function
	// upon the service request.
	ros::ServiceServer ros_tutorials_service_server = nh.advertiseService("ros_tutorial_srv",
	calculation);
	ROS_INFO("ready srv server!");

	ros::Rate r(10);  // 10hz
	while(1) {
		// Select the operator according to the value received from the parameter
		nh.getParam("calculation_method", g_operator);
		ros::spinOnce();  // Callback function process routine
		r.sleep();  // Sleep for routine iteration
	}

	//ros::spin();
						
	// Wait for the service request
	return 0;
}