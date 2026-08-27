while True:
    try:
        weight = float(input('Please enter your weight in kilograms: '))
        height = float(input('Please enter your height in meters: '))
        if weight <= 0 or height <= 0:
            print("Weight and height must be positive numbers. Please try again.")
            continue
        break
    except ValueError:
        print("Invalid input. Please enter numeric values for weight and height.")
        
BMI = weight / (height ** 2)

if BMI < 18.5:
    print(f'Your BMI is {BMI:.2f}. You are underweight.')   
elif BMI < 25.0:
    print(f'Your BMI is {BMI:.2f}. You have a normal weight.')
elif BMI < 30.0:
    print(f'Your BMI is {BMI:.2f}. You are overweight.')
else:
    print(f'Your BMI is {BMI:.2f}. You are obese.')