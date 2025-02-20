# Animal-Footprint-Classifier
                                        
Home Page

![Image](https://github.com/user-attachments/assets/0c167652-94d0-4f37-bb20-6ec123403154)

Introdution page 

![Image](https://github.com/user-attachments/assets/6db27df1-e020-46b1-aa08-a85d7b4cf6c3)
![Image](https://github.com/user-attachments/assets/c6acb7f4-7ce8-4c43-a723-1ec2c637e760)

Login page

![Image](https://github.com/user-attachments/assets/8f9345df-92e3-449c-8376-9211c2b55e38)

The backend interface for uploading Footprints

![Image](https://github.com/user-attachments/assets/117de827-f7cb-49ea-8753-cbc0f0ca94d5)

 Result of the image

![Image](https://github.com/user-attachments/assets/48dfd27c-f0fb-4646-8b70-20f2207ec6f3)

## Follow these steps to set up the environment and run the project:

1. Open a new terminal (Command Prompt, PowerShell, or Terminal of your choice).

2. Set the execution policy to allow the activation of the virtual environment (only required on Windows PowerShell):

   ```powershell
   Set-ExecutionPolicy Unrestricted -Scope Process

3.Create a virtual environment:

```cmd
python -m venv myenv


4.Activate the virtual environment:

On Windows (Command Prompt):

```cmd
myenv\Scripts\activate

On macOS/Linux:

```bash
source myenv/bin/activate


5.Install the required libraries:

```cmd
pip install -r requirements.txt


6.Run the application (Start the Streamlit app):

```cmd
streamlit run app.py
