import logging
import threading
import time

"""
Student: Thomas Welborn (tdw058)
Prof/Course: Dr. Smith COSC 4327 Operating Systems
Assignment 05 - Candy
Due: April 16, 2021

Purpose: This program explores Semaphores in Python.

Instructions: A group of N faculty members are sitting around a bowl of candy,
which holds M pieces of candy.  Each of the N faculty members spends his life
thinking and eating candy.  They must have a piece of candy to think.  One Teaching
Assistant spends his life sleeping except that when the bowl is empty he is woken up
and completely fills the candy bowl.  Only one faculty member can access the bowl at a time.

References:
[1] Course Lectures/Notes
[2] logging Python Documentation, Available:[https://docs.python.org/3/library/logging.html]
[3] threading Python Documentation, Available:[https://docs.python.org/3/library/threading.html]
[4] time Python Documentation, Available:[https://docs.python.org/3/library/time.html]
[5] "Synchronization by using Semaphores in Python", Available:[https://www.geeksforgeeks.org/synchronization-by-using-semaphore-in-python/]
[6] Global Variables, Available:https://stackoverflow.com/questions/855493/referenced-before-assignment-error-in-python
"""

'''
This function will be what the consumer threads run.
'''
def consumer_function(name):
    global mySem
    global candySem
    global bowl_size
    global candyInBowl
    global faculty_num
    global numFacultyThinking

    
    logging.info("Thread %s: starting", name)
    
    candySem.acquire()
    logging.info("Thread %s: candySem acquired", name)

    mySem.acquire()
    logging.info("Thread %s: mySem acquired, accessing crit section", name)
    candyInBowl -=1
    numFacultyThinking += 1
    logging.info("Thread %s: Ate one piece of candy. Now thinking...", name)
    
    mySem.release()
    logging.info("Thread %s: finishing", name)


'''
This function is what the one producer thread runs.
'''
def producer_function(name):
    global mySem
    global candySem
    global bowl_size
    global candyInBowl
    global faculty_num
    global numFacultyThinking

    
    logging.info("Thread %s: starting", name)
    while(numFacultyThinking != faculty_num):
        
        mySem.acquire()
        logging.info("Thread %s: mySem acquired", name)
        if (candyInBowl == 0):
            logging.info("Thread %s: Candy in bowl is 0! D:", name)
            candyInBowl = bowl_size
            for i in range(bowl_size):
                candySem.release()
            logging.info("Thread %s: Candy bowl has been filled :)", name)
        else:
            logging.info("Thread %s: Candy bowl is not empty. Continuing to sleep.", name)
        mySem.release()
        logging.info("Thread %s: mySem released", name)
        time.sleep(4)
    logging.info("Thread %s: finishing because all faculty are thinking", name)
    

def main():
    global mySem
    global candySem
    global bowl_size
    global candyInBowl
    global faculty_num
    global numFacultyThinking

    
    candyInBowl = 0
    numFacultyThinking = 0
    faculty_num = int(input("Enter the number of faculty: "))
    bowl_size = int(input("Enter the amount of candy the bowl can hold: "))
    # Initialize semaphore to 1 so that only 1 faculty can access bowl at a time
    mySem = threading.Semaphore(value=1)
    # Initialize candy bowl buffer
    candySem = threading.Semaphore(value=0)
    
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    
    logging.info("Main: Before creating threads.")
    threadList = []
    for i in range(faculty_num):
        x = threading.Thread(target=consumer_function, args=(i,))
        threadList.append(x)

    producer = threading.Thread(target=producer_function, args=('Producer',))

    logging.info("Main: Threads created. Before running any threads.")


    for i in range(len(threadList)):
        threadList[i].start()
    producer.start()
    
    
    logging.info("Main: Threads started, waiting for them to finish")

            
    for i in range(len(threadList)):
        threadList[i].join()
    producer.join()           

    logging.info("Main: All threads finished, all faculty have candy and are thinking")
    

    
if __name__ == '__main__':
    main()
