// Sample data for the table
const tableData = [];

for (let i = 1; i <= 25; i++) {
  tableData.push({
    key: i,
    id: `ID${12345 + i}`,
    name: ['Emma Wilson', 'Stephanie Nolan', 'Morgan Russel', 'Lindsley Liam', 'Ashley Baker Jr.'][i % 5],
    address: `1234 Main Street, Baton Rouge, LA ${70800 + i}`,
    goal: [
      'I will eat at least one food from each food group per day.',
      'Practice mindful eating at one meal per day.',
      'Establish a consistent morning routine that includes 10 minutes of stretching.',
      'Complete a 15-minute full-body strength workout 3 times a week.',
      'Engage in a low-impact cardio activity (e.g., walking, swimming) for 30 minutes, 4 times a week.',
      'Keep a detailed food and mood journal for at least one week to identify patterns.',
      'Dedicate 10 minutes daily to guided meditation or mindfulness exercises.',
      'Create and follow a nighttime wind-down routine to improve sleep quality.',
    ][i % 8],
    category: ['Nutritional', 'Behavioral', 'Activity'][i % 3],
    logDate: `07/${10 + (i % 5)}/2026 ${8 + Math.floor(i/4)}:${15 + (i%4 * 10)} ${i % 2 === 0 ? 'AM' : 'PM'}`,
  });
}

export default tableData;
