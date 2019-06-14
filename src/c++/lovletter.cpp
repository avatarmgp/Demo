#include <iostream>
#include <string>
#include <thread>
using namespace std;

//person class
class Person
{
private:
	std::string name;  //name of person
	std::string state;  //state of person

public:
	//default constructor
	Person(std::string source_name, std::string source_state = std::string()) : name(source_name), state(source_state) {}

	//member function: self
	//return his or her own name.
	std::string self()
	{
		return name;
	}

	//member function: met
	//return name of person he or she met.
	std::string met(Person another_person)
	{
		return another_person.self();
	}

	//member function: wait
	//apparently, if a person is alone,
	//he or she is waiting for someone.
	bool wait()
	{
		return (state == std::string("alone"));
	}
};

void thread_function1(const Person& data) 
{
    while(true)
    {
        cout << "wait" << endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    }
}

void thread_function2(const Person& data) 
{
    while(true)
    {
        cout << "wait" << endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    }
}

int main()
{
    int year = 1988;
    std::string born = "hello world";
    while (true)
    {
        switch(year)
        {
        case 1988:
        {
            Person I = { "Gopal", "alone" };
            std::thread thrObj1(&thread_function1,std::ref(I));
        }
        case 1992:
        {
            Person U = { "Brown", "alone" };
            std::thread thrObj2(&thread_function2,std::ref(U));
        }
        case 2018:
        {
            
        }
        case 2019:
        {

        }
        default:
            break;
        }

        std::cout << "year by year" << std::endl;
        year++;
    }

    /*//long long ago, I was alone, and I did not know you.
    long long ago;
	
	while (I.wait())  //for all these years, I have been waiting for someone.
	{
		if (I.met(you) == you.self())  //but since the time I met you,
		{
			std::cout << "Hello, world." << std::endl;  //I found that I actually met the whole world.
			return;
		}
	}*/

	return 0;
}