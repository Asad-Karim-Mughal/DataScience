import numpy as np

arr2d1 = np.array([1, 20])

print(arr2d1)
arr2d = np.arange((64)).reshape(8,8)
print(arr2d)

print(arr2d[::-2])


# # Original array
# original_array = np.array([1, 2, 3, 4, 5])

# # Create a copy
# copied_array = np.copy(original_array)

# # Modify the copy
# copied_array[0] = 10

# print("Original Array:", original_array)
# print("Copied Array:", copied_array)


a = np.array([[[[[[[[[[[[[[100]]]]]]]]]]]]]])

print(a.ndim)


arr = np.array(range(20))

print(arr)


print(arr[arr%5==0])


print(arr[arr%2==0])  ## even numbers without using loop

print(arr[arr%2!=0]) ## odd numbers without using loop

print([(arr > 5) & (arr < 15)])



arr2 = np.arange(36).reshape(6,6) ## showing true and false 


print(arr2)

print(arr2.T) # making row into column 

from PIL import Image


image = Image.open("asad.jpg")

print(f"format: {image.format}")
print(f"format: {image.size}")
print(f"format: {image.mode}")



numpydata = np.asarray(image)

print(numpydata.ndim)





