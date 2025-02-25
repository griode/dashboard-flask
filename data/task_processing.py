import pandas as pd
import seaborn as sns
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib
from config.mogodb_connect import init_mongodb
matplotlib.use('Agg')  # Set the backend to 'Agg' before importing pyplot


db = init_mongodb()

def plot_tasks() -> str:
    tasks = get_tasks() 

    if len(tasks) == 0:
        return ''
    
    df = pd.DataFrame(get_tasks())  # Get tasks from MongoDB
    df['status'] = df['status'].apply(lambda x: x.lower())  # Convert status to lowercase
    plt.figure(figsize=(10, 4))  # Set figure size
    ax = sns.barplot(x='status', y='progress', data=df, palette='viridis')  # Use a color palette for different colors
    plt.tight_layout()  # Adjust layout to prevent label cutoff
    
    # Remove the borders
    sns.despine(bottom=True, left=True)
    
    # Save the plot to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    buffer.seek(0)
    
    # Encode the BytesIO object to base64
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return img_base64


def add_task(task: dict):
    try:
        # Insert into tasks collection
        result = db.get_collection('tasks').insert_one(task)
        print(f"Task inserted with id: {result.inserted_id}")
        return True
    except Exception as e:
        print(f"Error inserting task: {e}")
        return False
   
    
def get_tasks():
    try:
        # Fetch all tasks from collection
        tasks = list(db.get_collection('tasks').find({}, {'_id': 0}))  # Exclude MongoDB _id field
        return tasks
    except Exception as e:
        print(f"Error fetching tasks: {e}")
        return []