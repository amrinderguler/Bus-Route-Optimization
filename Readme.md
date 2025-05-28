# Bus Route Optimization

A full-stack application for optimizing school bus routes using uploaded CSV files for buses and students. The project features a Next.js/React frontend and a Python Flask backend.

## Features

- Upload bus and student CSV files
- Server-side route optimization (mock/demo or real algorithm)
- Download optimized route CSVs for each bus
- Download a summary CSV for all buses
- Responsive, modern UI with Tailwind CSS

## Folder Structure
```markdown
# Bus Route Optimization

A full-stack application for optimizing school bus routes using uploaded CSV files for buses and students. The project features a Next.js/React frontend and a Python Flask backend.

## Features

- Upload bus and student CSV files
- Server-side route optimization (mock/demo or real algorithm)
- Download optimized route CSVs for each bus
- Download a summary CSV for all buses
- Responsive, modern UI with Tailwind CSS

## Folder Structure

```
Bus_Route_optimization/
├── Assets/
│   ├── bus (1).csv
│   └── stud.csv
├── backend/
│   ├── main.py
│   ├── requirement.txt
│   └── results/
├── frontend/
│   ├── app/
│   ├── components/
│   ├── public/
│   ├── styles/
│   ├── package.json
│   └── ...
└── README.md
```

### Assets Folder

The `Assets` folder contains sample CSV files for buses and students:
- **bus (1).csv**: Example bus data (bus number, latitude, longitude, capacity, mileage)
- **stud.csv**: Example student data (student ID, name, latitude, longitude, pickup point)

You can use these files to test the application or as templates for your own data.

## Getting Started

### Prerequisites

- Node.js (v18+ recommended)
- Python 3.8+
- pip

### Backend Setup

1. Navigate to the backend folder:
    ```sh
    cd backend
    ```
2. Install dependencies:
    ```sh
    pip install -r requirement.txt
    ```
3. Run the Flask server:
    ```sh
    python main.py
    ```

### Frontend Setup

1. Navigate to the frontend folder:
    ```sh
    cd frontend
    ```
2. Install dependencies:
    ```sh
    npm install
    ```
3. Run the Next.js development server:
    ```sh
    npm run dev
    ```

### Usage

1. Open the frontend in your browser (usually at [http://localhost:3000](http://localhost:3000)).
2. Upload your bus and student CSV files (you can use the files in the `Assets` folder).
3. Click "Optimize Routes".
4. Download the optimized route CSVs for each bus or the summary CSV from the "Summary" tab.

## Development

- Frontend: [Next.js](https://nextjs.org/), [React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/)
- Backend: [Flask](https://flask.palletsprojects.com/), [pandas](https://pandas.pydata.org/), [numpy](https://numpy.org/)

## Customization

- To implement your own optimization logic, modify `backend/main.py`.
- To change the UI, edit files in `frontend/app` and `frontend/components`.