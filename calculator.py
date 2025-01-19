import streamlit as st, re
# Function to handle operations
def calculate(num1, num2, operation):
    try:
        if operation == "Addition(+)":
            return num1 + num2
        if operation == "Subtraction(-)":
            return num1 - num2
        if operation == "Multiplication(*)":
            return num1 * num2
        if operation == "Division(/)":
            if num2 == 0:
                st.error("**Warning: You are trying to divide by zero!**")
            return num1 / num2
        if operation == "Modulus Division(%)":
            if num2 == 0:
                st.error("**Warning: You are trying to divide by zero!**")
            return num1 % num2
        if operation == "Exponentiation(^)":
            if num1 >= 100 or num2 >= 100:  # Limit for exponentiation
                return "Result too large to compute."
            return num1 ** num2
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit app
def main():
    st.set_page_config(
    page_title="BASIC CALCULATOR",  
    page_icon="🧮",                  
    layout="wide")
    st.title(":rainbow[Basic Calculator]")
    st.write("""This application is designed to perform fundamental arithmetic operations.
             This app is perfect for quick and simple calculations in an interactive format!""")
    
    a, b = st.columns(2)
    with a:
        st.markdown("""### :blue[Features:]""")
        st.markdown("""
        - :rainbow[Input Two Numbers:] Users can enter two numbers using numeric input fields.
        - :rainbow[Select an Operation:] A dropdown menu lets users choose operations like:
            - Addition (+)
            - Subtraction (-)
            - Multiplication (*)
            - Division (/)
            - Modulus (%)
            - Exponentiation (^)
        - :rainbow[View Results:] Click the 'Calculate' button to display the result, styled with custom formatting.
        ### :blue[Key Features:]
        - :rainbow[User-friendly Interface:] Inputs and outputs are neatly separated for clarity.
        - :rainbow[Error Handling:] Division by zero is gracefully handled with appropriate warnings & Avoids invalid inputs.""")

    with b:
        c, d = st.columns(2)
        with c:
            st.warning(":red[**🌱INPUT💧SECTION☀️**]")
            # Get user input
            st.write("__Enter two numbers and select an operation.__")
            num1 = st.number_input("Enter first number")
            num2 = st.number_input("Enter second number")
            operation = st.selectbox("Choose an operation", ["Addition(+)", "Subtraction(-)", "Multiplication(*)", "Division(/)", "Modulus Division(%)", "Exponentiation(^)"])

        with d:
            st.warning(":red[**🌳OUTPUT SECTION🌳**]")
            operator_match = re.search(r'([+\-*/%^])', operation)
            operator = operator_match.group(0) if operator_match else "Invalid"
            # Print output
            if st.button(":green[**Calculate**]"):
                result = calculate(num1, num2, operation)
                st.markdown(f"<h2 style='font-size: 20px;background-color:green; color: white; padding: 10px;'>The result of {num1} {operator} {num2} is: {result}</h2>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
