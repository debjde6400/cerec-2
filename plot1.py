import matplotlib.pyplot as plt

x = [0,1,2,3,4,5]

plt.plot(x)
plt.show()

x = [1,2,3]
y = [5,7,4]

x2 = [1,2,3]
y2 = [10,14,12]

plt.plot(x,y, label = 'First Line')
plt.plot(x2,y2, label = 'Second Line')

plt.xlabel('Plot Number')
plt.ylabel('Important var')

plt.title('Interesting Graph\nCheck check shirt')
plt.show()

x3 = [1,2,3,4,5,6,7,8]
y3 = [5,2,4,2,1,4,5,2]

plt.scatter(x3, y3, label = 'skitscat',
 color='k', marker='*', s=100.0)

plt.xlabel('Plot Number')
plt.ylabel('Important var')
plt.legend()
plt.title('Interesting Graph\nCheck check shirt')
plt.show()