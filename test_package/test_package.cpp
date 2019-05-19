#include <cppkafka/cppkafka.h>
#include <iostream>

using namespace std;
using namespace cppkafka;

int main() {
    // Create the config
    Configuration config = {
        { "metadata.broker.list", "127.0.0.1:9092" }
    };
     try {
   	// Create the producer
    	Producer producer(config);

    	// Produce a message!
    	string message = "hey there!";
   	producer.produce(MessageBuilder("my_topic").partition(0).payload(message));
    	producer.flush();
    }
    catch (const Exception& ex) {
        cout << "Error fetching metadata: " << ex.what() << endl;
    }    
}
