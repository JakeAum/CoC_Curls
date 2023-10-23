#starting lists of a few possibleworkouts depending on the day and workout needs.

#intermediate arms excersises
armsInter = ['Dumbell biceps curl','Dumbell hammer curl'
             'Cable Rope Curl','Bench Body weight triceps dips',
             'Cable Triceps Pushdown']
#medium difficult arm exercises

armsMed = ['Push-ups','Bent over row','Lying Chest Press','Rear deltoid fly',
           'Push press','Skull Crushers','Cable Chest fly','Pull ups']

#more advanced arm excerises, maybe add a prompt that says to add more reps?
armsAdvan = ['Dead hang', 'Barbell Curls','High Cable Tricep Pushdown','Overhead Bicep Cable Curls',
             'Low Cable Bicep Curls','Barbell Overhead Tricep Extensions',
             'Rope Tricep Extension','Alternate Dumbell Hammer Curl','Machine Preacher Curl']
#begining of leg exervises
legsInter = ['Body weight Squats','Leg Press','Lunges','Leg Curls','Deadlift',
             'Step-up','Incline Treadmil Walk','Leg Extensions']
#medium difficulty legs
legsMed = ['Barbell Back Squat','Romainian Deadlift','Dumbbell Lunge','Goblet Squat',
           'Standing Calf Raise','Barbell Hip Thrust','Barbell Hip Thrust']
#advanced leg workouts
legsAdvan = ['Stair-master','Side Lunge','Box Jump','Jumping Lunge',
             'Bulgarian Split Squat','Sumo Squat','Weighted Donkey Calf Raise']

#func to rest all code
def run():
    print(legsInter)
    print(legsMed)
    return legsAdvan

print(run())