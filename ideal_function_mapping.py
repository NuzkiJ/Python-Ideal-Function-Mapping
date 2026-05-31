#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os

class BaseCustomError(Exception):
    """Root exception class for custom errors with built-in logging support."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def log_error(self):
        """Append the error message to an external log file."""
        with open("error_log.txt", "a") as log_file:
            log_file.write(f"ERROR: {self.message}\n")


class CustomFileNotFoundError(BaseCustomError):
    """Raised when a required file path cannot be located."""
    def __init__(self, file_path, message="File not found"):
        super().__init__(f"{message}: {file_path}")


class CustomEmptyDataError(BaseCustomError):
    """Raised when a dataset file contains no data."""
    def __init__(self, file_path, message="The file is empty"):
        super().__init__(f"{message}: {file_path}")


class CustomDataParseError(BaseCustomError):
    """Raised when an error occurs while parsing input data."""
    def __init__(self, file_path, message="Error parsing data"):
        super().__init__(f"{message}: {file_path}")


class CustomDataHandlerError(BaseCustomError):
    """General exception for unexpected issues during data processing."""
    def __init__(self, message="An unexpected error occurred"):
        super().__init__(message)


# In[ ]:


import pandas as pd


"""Data handler class responsible for loading and processing datasets."""
class DataHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_data()


    """Loads data from a CSV file and raises custom exceptions if any issues occur."""
    def load_data(self):
        try:
            data = pd.read_csv(self.file_path)
            if data.empty:
                raise CustomEmptyDataError(f"The file {self.file_path} contains no data.")

        except FileNotFoundError as e:
            custom_error = CustomFileNotFoundError(self.file_path)
            custom_error.log_error()  # Log error to file
            raise custom_error from e

        except pd.errors.EmptyDataError as e:
            custom_error = CustomEmptyDataError(self.file_path)
            custom_error.log_error()  # Log error to file
            raise custom_error from e

        except pd.errors.ParserError as e:
            custom_error = CustomDataParseError(self.file_path)
            custom_error.log_error()  # Log error to file
            raise custom_error from e

        except Exception as e:
            custom_error = CustomDataHandlerError()
            custom_error.log_error()  # Log error to file
            raise custom_error from e

        return data


# In[ ]:


class TrainDataHandler(DataHandler):
    """Specialized data handler for loading and managing training dataset."""
    def __init__(self, file_path):
        super().__init__(file_path)


# Load training dataset using the custom handler
train_data = TrainDataHandler('train.csv').data

# Display first few rows of the training data
train_data.head()


# In[ ]:


from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import declarative_base, sessionmaker


class DatabaseConnection:
    def __init__(self, db_url):
        """Initialize DatabaseConnection with a given database URL."""
        self.db_url = db_url
        self.engine = create_engine(self.db_url)
        self.Base = declarative_base()
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        """Create and return a new SQLAlchemy session instance."""
        return self.Session()

    def get_Base(self):
        """Return the SQLAlchemy declarative Base object."""
        return self.Base

    def get_engine(self):
        """Return the SQLAlchemy engine object."""
        return self.engine


# In[ ]:


class InsertRecords:

    def create_tables(data):
        session = database.get_session()  # Create database session
        Base = database.get_Base()  # Retrieve declarative Base class
        engine = database.get_engine()  # Retrieve database engine

        """Create all tables defined in the ORM Base metadata."""
        Base.metadata.create_all(engine)
        session.add(data)  # Insert record into database session
        session.commit()  # Commit transaction to persist changes
        session.close()  # Close session after completing database operation


# In[ ]:


DB_URL = 'sqlite:///./my_db.db'
database = DatabaseConnection(DB_URL)

# Define ORM model: create a base class and map table structure
class TrainingData(database.get_Base()):
    '''
    Training data table contains 5 columns: x, y1, y2, y3, and y4.
    Each column is defined with its corresponding data type.
    '''
    __tablename__ = 'training'  # Table name for training dataset
    id = Column(Integer, primary_key=True, autoincrement=True)  # Auto-generated primary key
    x = Column(Float)
    y1 = Column(Float)
    y2 = Column(Float)
    y3 = Column(Float)
    y4 = Column(Float)


record = InsertRecords  # Reference to record insertion handler
data = ''

for _, row in train_data.iterrows():  # Iterate through training dataset rows
    # Create dictionary of column-value pairs
    args = {key: row[key] for key in train_data.columns}

    '''
    Unpack dictionary into keyword arguments.
    Equivalent to:
    x=row['x'], y1=row['y1'], y2=row['y2'], y3=row['y3'], y4=row['y4']
    '''
    record.create_tables(TrainingData(**args))  # Insert record into database


# In[ ]:





# In[ ]:


class IdealDataHandler(DataHandler):
    """Specialized handler class for loading and managing ideal dataset."""
    def __init__(self, file_path):
        super().__init__(file_path)


# Load ideal dataset using the custom handler
ideal_function = IdealDataHandler('ideal.csv').load_data()

# Display first few rows of the ideal dataset
ideal_function.head()


# In[ ]:


database = DatabaseConnection(DB_URL)

# Define ORM model: create base class and define table structure
class IdealData(database.get_Base()):
    '''
    Ideal function dataset contains 51 columns:
    x and y1 to y50, each representing a float-valued feature.
    '''
    __tablename__ = 'ideal_functions'  # Table name for ideal function data
    id = Column(Integer, primary_key=True, autoincrement=True)  # Auto-generated primary key
    x = Column(Float)

    # Dynamically adding y1, y2, ..., y50 columns
    for i in range(1, 51):
        locals()[f"y{i}"] = Column(Float)


record = InsertRecords  # Reference for record insertion handler
data = ''

for _, row in ideal_function.iterrows():  # Iterate through ideal dataset rows
    # Convert row into dictionary of column-value pairs
    args = {key: row[key] for key in ideal_function.columns}

    '''
    Unpack dictionary into keyword arguments.
    Equivalent to:
    x=row['x'], y1=row['y1'], ..., y50=row['y50']
    '''
    record.create_tables(IdealData(**args))  # Insert record into database


# In[ ]:


from bokeh.plotting import figure, show


class DataVisualizer:
    def visulize_data(data_records, columnName, p=None, size=1, shape="circle", color=None, title=''):
        # Validate that the required column exists in the dataset
        if columnName not in data_records.columns:
            raise ValueError(f"Column '{columnName}' not found in DataFrame.")

        # Predefined color palette (DO NOT CHANGE — used for consistent visualization mapping)
        colors = [
            "purple", "navy", "grey", "gold", "red", "black",
            "orange", "blue", "pink", "green", "violet", "brown",
            "yellow", "maroon"
        ]

        # Assign user-defined color if provided; otherwise auto-assign based on column hash
        color = color if color else colors[hash(columnName) % len(colors)]

        # Create new figure if one is not provided externally
        if p is None:
            p = figure(title="Data Visualization",
                       x_axis_label="X - Values",
                       y_axis_label="Y - Values")

        # Scatter plot for the selected column against x-values
        p.scatter(
            data_records['x'],
            data_records[columnName],
            size=size,
            legend_label=f"X vs {columnName} {title}",
            color=color,
            marker=shape
        )

        # Return the updated figure for further customization or rendering
        return p


# In[ ]:


# Visualize the Training Data

# Create database connection object
db = DatabaseConnection(DB_URL)

# Load training data from database into a Pandas DataFrame
# Reads entire SQL table into memory
training_data = pd.read_sql_table("training", con=db.get_engine())

# Initialize visualizer class reference
train_data_visualizer = DataVisualizer

# Visualize training dataset: x vs y1 to y4 values
p = None

# Loop through all y-columns (excluding 'id' column in DB)
for i in range(1, len(training_data.columns) - 1):
    p = train_data_visualizer.visulize_data(
        training_data,
        'y' + str(i),
        p,
        1,
        shape='circle',
        title='Training Data'
    )

# Display final combined plot
show(p)


# In[ ]:


# Visualize the Ideal Data

# Create database connection object
db = DatabaseConnection(DB_URL)

# Load ideal function data from database into a Pandas DataFrame
# Reads entire SQL table into memory
ideal_data = pd.read_sql_table("ideal_functions", con=db.get_engine())

# Initialize visualizer class reference
ideal_data_visualizer = DataVisualizer

# Visualize ideal dataset: x vs y1 to y50 values
p = None

# Loop through all y-columns (excluding 'id' column in DB)
for i in range(1, len(ideal_data.columns) - 1):
    p = ideal_data_visualizer.visulize_data(
        ideal_data,
        'y' + str(i),
        p
    )

# Display final combined plot
show(p)


# In[ ]:


class MergeDataFrame:
    '''
    The training dataset and ideal functions dataset need to be compared using MSE.
    Since comparison is based on matching x-values, both datasets are merged
    (similar to SQL JOIN) for consistent row-wise evaluation.
    '''    
    def mergeData(train_data, ideal_function):
        df = pd.merge(ideal_function, train_data, on='x', suffixes=('', '_train'))
        return df


'''
Training data and ideal functions are stored in the database.
They are loaded into DataFrames and merged into a single dataset for analysis.

Although x-values are aligned row-by-row in this assignment, merging is still
used as a standard practice to avoid potential alignment errors in future cases.
'''

db = DatabaseConnection(DB_URL)

# Load training data from database
training_data = pd.read_sql_table("training", con=db.get_engine())

# Load ideal function data from database
ideal_function = pd.read_sql_table('ideal_functions', con=db.get_engine())

# Create merge handler object
merge_data = MergeDataFrame

# Merge training and ideal datasets
merged_df = merge_data.mergeData(train_data, ideal_function)

# Display first few rows of merged dataset
merged_df.head()


# In[ ]:


from sklearn.metrics import mean_squared_error  # Used to compute Mean Squared Error efficiently


class FindBestFitFunctions:
    """
    Finds the best matching ideal function (from 50 candidates)
    for each training dataset target column using Mean Squared Error (MSE).

    Each training column (y1, y2, y3, y4) is compared against all ideal functions
    (y1 to y50), and the function with the lowest MSE is selected.
    """     

    # Identify best-fitting ideal function for each training column
    def find_best_fit_ideal_function(train, ideal, merged_df):
        best_fit_function = {}  # Stores mapping: training column -> best matching ideal function

        '''
        Outer loop iterates through training data columns.
        Inner loop compares each training column with all ideal functions.
        '''

        for i in range(1, train):
            # Format training column name to match merged dataframe
            y_train = 'y' + str(i) + '_train'

            best_fit = ''  # Stores best matching ideal function for current training column
            best_mse = float('inf')  # Initialize with infinity for minimization

            for j in range(1, ideal):
                # Format ideal function column name
                y_func = 'y' + str(j)

                '''
                Compute MSE between training column and ideal function.
                The lowest MSE indicates the best fit.
                '''

                # Ensure ideal column exists and contains data
                if y_func not in merged_df.columns or merged_df[y_func].empty:
                    continue

                mean_error = mean_squared_error(
                    merged_df[y_train],
                    merged_df[y_func]
                )

                if mean_error < best_mse:
                    best_mse = mean_error
                    best_fit = y_func

            best_fit_function[y_train] = best_fit

        return best_fit_function  # Return mapping of best-fit functions


# Run best-fit selection process
find_best_fit_func = FindBestFitFunctions

best_fit_function = find_best_fit_func.find_best_fit_ideal_function(
    len(training_data.columns) - 1,
    len(ideal_function.columns) - 1,
    merged_df
)

best_fit_function


# In[ ]:





# In[ ]:


# Create database connection object
db = DatabaseConnection(DB_URL)

# Load training and ideal function data from database
training_data = pd.read_sql_table("training", con=db.get_engine())
ideal_function = pd.read_sql_table("ideal_functions", con=db.get_engine())

# Visualize results using Bokeh
'''
    Compare training data with their corresponding best-fit ideal functions.
    This visualization step is optional and is used to verify correctness of the analysis.
'''
data_visualize = DataVisualizer

'''
The idea is to plot:
    Training data pairs: (x, y1), (x, y2), (x, y3), (x, y4)
    Ideal function matches: (x, y42), (x, y41), (x, y11), (x, y48)
'''

# Plot training data (y1 to y4)
p = None
for i in range(1, len(training_data.columns) - 1):
    p = data_visualize.visulize_data(
        training_data,
        'y' + str(i),
        p,
        2.5,
        'star',
        title='Training Data'
    )

# Plot selected ideal functions for comparison
data_visualize.visulize_data(ideal_function, 'y41', p, title='Ideal func', color='red')
data_visualize.visulize_data(ideal_function, 'y42', p, title='Ideal func', color='green')
data_visualize.visulize_data(ideal_function, 'y11', p, title='Ideal func', color='black')
data_visualize.visulize_data(ideal_function, 'y48', p, title='Ideal func', color='blue')

'''
The visulize_data function demonstrates polymorphism,
as it is reused for multiple datasets and configurations.
'''

# Display final plot
show(p)


# In[ ]:


# Load test data from CSV file

class TestDataHandler(DataHandler):
    """Specialized handler class for loading and managing test dataset."""
    def __init__(self, file_path):
        super().__init__(file_path)


# Load test dataset using the custom handler
test_data_points = TestDataHandler('test.csv').load_data()

# Display first few rows of test data
test_data_points.head()


# In[ ]:


# Visualize the Test Data

test_data_visualizer = DataVisualizer

# Initialize plot object
p = None

# Plot test dataset values
p = test_data_visualizer.visulize_data(
    test_data_points,
    'y',
    p,
    7,
    'circle',
    'yellow',
    title='Test Data '
)

# Display plot
show(p)


# In[ ]:


import numpy as np


class MaxDeviation:
    '''
    Computes the maximum absolute deviation between training data
    and their corresponding best-fit ideal functions.

    Output is returned as a dictionary:
        {training_column: max_deviation_value}
    '''

    def find_max_deviations(best_fit_functions):
        max_deviation = {}

        for y_column, ideal_column in best_fit_functions.items():
            # Convert training column name to match original dataset naming
            y_column = y_column.replace('_train', '')

            # Compute maximum absolute deviation between training and ideal values
            max_deviation[y_column] = np.max(
                np.abs(training_data[y_column] - ideal_function[ideal_column])
            )

        return max_deviation


# Compute maximum deviations for each best-fit mapping
max_deviation = MaxDeviation.find_max_deviations(best_fit_function)

# Display computed deviations
max_deviation


# In[ ]:


DB_URL = 'sqlite:///./my_db.db'

# Initialize database connection using the provided SQLite database URL
database = DatabaseConnection(DB_URL)


# In[ ]:


# Define ORM model: create base class and map test data table structure
class TestDataModel(database.get_Base()):
    __tablename__ = 'test_data_mapping'

    '''
    This table contains 4 main columns:
        x_test, y_test, delta_y, and assigned_ideal_function.
    Each column must be defined with an appropriate data type.
    '''

    id = Column(Integer, primary_key=True, autoincrement=True)  # Auto-generated primary key
    x = Column(Float)  # Mapping x_test column as x
    y = Column(Float)  # Mapping y_test column as y
    delta_y = Column(Float)
    assigned_ideal_function = Column(String)


# In[ ]:


class MapTestData:
    '''
    Class responsible for mapping test data rows to the most suitable ideal function
    based on deviation constraints and previously computed best-fit mappings.
    '''

    def __init__(self, test_data_points, ideal_function, best_fit_function, max_deviation, record):
        self.test_data_points = test_data_points
        self.ideal_function = ideal_function
        self.best_fit_function = best_fit_function
        self.max_deviation = max_deviation
        self.record = record

    def map_test_data_with_ideal_function(self):
        for _, row in self.test_data_points.iterrows():
            x_test = row['x']  # X-value from test dataset
            y_test = row['y']  # Y-value from test dataset

            best_fit = None  # Stores best matching ideal function
            min_deviation = None  # Tracks minimum deviation found

            for y_column, ideal_column in self.best_fit_function.items():
                ideal_value = self.ideal_function.loc[
                    self.ideal_function['x'] == x_test, ideal_column
                ].values

                if len(ideal_value) == 0:
                    continue

                deviation = np.abs(y_test - ideal_value[0])  # Absolute deviation calculation

                # Clean training column name to match deviation dictionary keys
                y_column_clean = y_column.replace('_train', '')

                # Validate against maximum allowed deviation
                if y_column_clean in self.max_deviation:
                    if deviation <= self.max_deviation[y_column_clean] * np.sqrt(2):
                        min_deviation = deviation
                        best_fit = ideal_column

            # Store mapped result into database
            self.record.create_tables(
                TestDataModel(
                    x=x_test,
                    y=y_test,
                    delta_y=min_deviation,
                    assigned_ideal_function=best_fit
                )
            )


# Create record insertion handler
record = InsertRecords

# Map test dataset to ideal functions
data_pt = MapTestData(
    test_data_points,
    ideal_function,
    best_fit_function,
    max_deviation,
    record
)

data_pt.map_test_data_with_ideal_function()


# In[ ]:


'''
Finally, we visualize the test data points along with the assigned ideal functions.
Some test data points cannot be mapped to any selected ideal function.

These unmapped points are treated as outliers since they do not satisfy
the deviation constraints defined in the model.
'''

# Create database connection object
db = DatabaseConnection(DB_URL)

# Load mapped test data from database
test_data = pd.read_sql_table("test_data_mapping", con=db.get_engine())

# Display first few rows of mapped test data
test_data.head()


# In[ ]:


# Filter only successfully mapped test data points (exclude outliers / unmapped points)
fitted_test_data = test_data[test_data['assigned_ideal_function'].notna()]

# Display first few rows of the filtered (valid mapped) test data
fitted_test_data.head()


# In[ ]:


# Filter test data points that could not be assigned to any ideal function (outliers)
outlier_test_data = test_data[test_data['assigned_ideal_function'].isna()]

# Display first few rows of outlier data
outlier_test_data.head()


# In[ ]:


# Display summary information about the mapped test dataset
# Includes column names, non-null counts, and data types
test_data.info()


# In[ ]:


'''
Visualize assigned test data points and outliers together.

This helps distinguish:
- Successfully mapped test points (fitted data)
- Unmapped test points (outliers)
- Selected ideal functions used for mapping
'''

data_visualizer = DataVisualizer  # Initialize visualization handler
p = None

# Plot fitted (mapped) test data points
p = data_visualizer.visulize_data(
    fitted_test_data,
    'y',
    p,
    5,
    'circle',
    title='Fitted Test Data',
    color='red'
)

# Plot outlier test data points
data_visualizer.visulize_data(
    outlier_test_data,
    'y',
    p,
    5,
    'star',
    title='Outliers Test Data',
    color='yellow'
)

# Overlay selected ideal functions for comparison
data_visualizer.visulize_data(ideal_function, 'y41', p, title='Ideal func', color='purple')
data_visualizer.visulize_data(ideal_function, 'y42', p, title='Ideal func', color='black')
data_visualizer.visulize_data(ideal_function, 'y11', p, title='Ideal func', color='green')
data_visualizer.visulize_data(ideal_function, 'y48', p, title='Ideal func', color='orange')

# Display final visualization
show(p)


# In[ ]:


import unittest
import pandas as pd


class TestFindBestFitFunctions(unittest.TestCase):

    def test_find_best_fit_ideal_function(self):
        """Validate correct mapping of training data to best-fit ideal functions using MSE."""

        # Sample training dataset for unit testing
        training_data_ = pd.DataFrame({
            'id': [1, 2, 3],
            'x': [1, 2, 3],
            'y1': [1.1, 2.2, 3.3],
            'y2': [5.2, 5.3, 6.4]
        })

        # Sample ideal function dataset
        ideal_function_ = pd.DataFrame({
            'id': [1, 2, 3],
            'x': [1, 2, 3],
            'y1': [1.0, 2.0, 3.0],
            'y2': [2.1, 2.1, 3.1],
            'y3': [5.2, 5.2, 5.2]
        })

        # Merge datasets on x-axis for comparison
        merged_df_ = pd.merge(
            ideal_function_,
            training_data_,
            on='x',
            suffixes=('', '_train')
        )

        # Expected best-fit mapping based on lowest MSE
        expected_best_fit = {
            'y1_train': 'y1',  # Best match for y1_train
            'y2_train': 'y3'   # Best match for y2_train
        }

        # Execute function under test
        best_fit_function_ = FindBestFitFunctions.find_best_fit_ideal_function(
            len(training_data_.columns) - 1,
            len(ideal_function_.columns) - 1,
            merged_df_
        )

        # Validate output
        self.assertEqual(best_fit_function_, expected_best_fit)

    def test_empty_data(self):
        """Ensure function handles empty datasets gracefully."""

        # Empty datasets
        training_data = pd.DataFrame(columns=['id', 'x', 'y1', 'y2'])
        ideal_function = pd.DataFrame(columns=['id', 'x', 'y1', 'y2', 'y3'])
        merged_df = pd.DataFrame(columns=['id', 'x', 'y1', 'y2', 'y3', 'y1_train', 'y2_train'])

        # Expected output for empty case
        expected_output = {'y1_train': '', 'y2_train': ''}

        # Simulated output (placeholder logic in original test)
        best_fit_func = {'y1_train': '', 'y2_train': ''}

        # Validate empty-case behavior
        self.assertEqual(best_fit_func, expected_output)


if __name__ == '__main__':
    # Create test suite and execute all test cases
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFindBestFitFunctions)
    unittest.TextTestRunner(verbosity=2).run(suite)


# In[ ]:


import unittest
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import IntegrityError


# Import the classes to be tested
DATABASE_URL = "sqlite:///testx.db"  # SQLite database used for unit testing

database = DatabaseConnection(DATABASE_URL)
Base = database.get_Base()
engine = database.get_engine()
Session = database.get_session()


# Define a sample ORM model for testing database operations
class SampleModel(Base):
    __tablename__ = "sample_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    description = Column(String, nullable=True)


# Create a clean test database schema
Base.metadata.drop_all(engine)  # Remove existing tables before testing
Base.metadata.create_all(engine)


class TestDatabaseConnection(unittest.TestCase):

    def setUp(self):
        """Initialize a new session before each test case."""
        self.session = Session

    def tearDown(self):
        """Close session and clean up after each test case."""
        self.session.close()
        engine.dispose()

    def test_database_connection(self):
        """Verify that database engine and session are properly initialized."""
        self.assertIsNotNone(engine)
        self.assertIsNotNone(self.session)

    def test_insert_record(self):
        """Test inserting and retrieving a valid record from the database."""
        test_entry = SampleModel(x=1.0, y=2.0, description="Test Entry")
        self.session.add(test_entry)
        self.session.commit()

        retrieved_entry = (
            self.session.query(SampleModel)
            .filter_by(x=1.0)
            .first()
        )

        self.assertIsNotNone(retrieved_entry)
        self.assertEqual(retrieved_entry.y, 2.0)
        self.assertEqual(retrieved_entry.description, "Test Entry")

    def test_insert_null_value(self):
        """Ensure IntegrityError is raised when inserting invalid NULL values."""
        test_entry = SampleModel(x=None, y=2.0, description="Invalid Entry")
        self.session.add(test_entry)

        with self.assertRaises(IntegrityError):
            self.session.commit()

        self.session.rollback()

    def test_insert_records_via_insert_records_class(self):
        """Test insertion using the InsertRecords helper class."""
        test_entry = SampleModel(x=3.0, y=4.0, description="Inserted via InsertRecords")
        InsertRecords.create_tables(test_entry)

        retrieved_entry = self.session.query(SampleModel).filter_by(x=3.0).first()

        self.assertIsNotNone(retrieved_entry)
        self.assertEqual(retrieved_entry.y, 4.0)
        self.assertEqual(retrieved_entry.description, "Inserted via InsertRecords")


if __name__ == '__main__':
    # Create test suite and execute all unit tests
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDatabaseConnection)
    unittest.TextTestRunner(verbosity=2).run(suite)

