def fuzzbuzz(n):
    for i in range(n+1) :
        print("Fuzz"*(i%3==0) + "Buzz"*(i%5==0) or i)

fuzzbuzz(100)
