#include<iostream>
using namespace std;

class Base
{
public:
    virtual void func()
    {
        cout << "Base" << endl;
    }
};

class Drived : public Base
{
public:
    void func()
    {
        cout << "Drived" << endl;
    }

    int a;
};

int main()
{
    Drived pd = Base();
    pd.func();

    return 0;
}