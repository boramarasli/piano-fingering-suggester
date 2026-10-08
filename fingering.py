#fingering.py- suggest right hand piano fingering for a melody 
# fingers 1= thumb ... 5= little finger (only for right hand)

import itertools 
#part 1 notes as numbers c4=60, one number per key 
NOTE_NUMBERS = {"C":0,"C#":1,"Db":1,"D":2,"D#":3,"Eb":3,"E":4,
                "F":5,"F#":6,"Gb":6,"G":7,"G#":8,"Ab":8,"A":9,
                "A#":10,"Bb":10,"B":11}
BLACK_KEYS = {1, 3, 6, 8, 10}

def to_midi(note): 
    """'C4' -> 60, 'F#4' -> 66."""
    name, octave = note[:-1], int(note[-1])
    return 12 * (octave + 1) + NOTE_NUMBERS[name]

def is_black(midi): 
    return midi % 12 in BLACK_KEYS


#the rules
#rule 1 - comfortable distance in keys between two fingers 
COMFORT = {
    (1, 2): (1, 5), (1, 3): (3, 7), (1,4): (5, 9), (1, 5): (7, 10), 
    (2, 3): (1, 2), (2, 4): (3, 4), (2, 5): (5, 6), 
    (3, 4): (1, 2), (3, 5): (3, 4),
    (4, 5): (1, 2), 
}

#rule 2 the thuymb can pass under fingers 2,3,4
CROSS_COST = {2: 2, 3: 1, 4: 2}

def move_cost(a, finger_a, b, finger_b): 
    """Cost of playing note b with finger_b right after note a with finger_a"""
    step = b - a # +going up -going down 
    cost = 0

    #Rule 4 the thumb on a black key is not the first pref. 
    if finger_b == 1 and is_black(b): 
        cost += 1 

    # Rule 3: the same finger on a new note can't be played smoothly
    if finger_a == finger_b: 
        return cost + (0 if step == 0 else 5)

    going_up = step > 0 
    normal_order = (going_up and finger_b > finger_a) or (not going_up and finger_b < finger_a)

    if normal_order: 
        #r1- too close or too far apart costs one point per key 
        low, high = COMFORT[(min(finger_a, finger_b), max(finger_a, finger_b))]
        distance = abs(step)
        if distance < low: 
            cost += low - distance 
        elif distance > high: 
            cost += distance - high 
        return cost 

    #r2 - crossing only the thumb can go under or be crossed over 
    other = finger_a if finger_b == 1 else finger_b 
    if 1 in (finger_a, finger_b) and other in CROSS_COST: 
        return cost + CROSS_COST[other] + max(0, abs(step)-4)
    return cost + 10 #any other crossing very awk.

def total_cost(notes, fingering): 
    cost = 1 if fingering[0] == 1 and is_black(notes[0]) else 0 
    for i in range(len(notes) - 1): 
        cost += move_cost(notes[i], fingering[i], notes[i+1], fingering[i+1])
    return cost 

# part 3 - brute foce trying every combination 
def brute_force(notes): 
    best, best_cost = None, None 
    for fingering in itertools.product([1, 2, 3, 4, 5], repeat=len(notes)):
        cost = total_cost(notes, fingering)
        if best_cost is None or cost < best_cost: 
            best, best_cost = list(fingering), cost 
    return best, best_cost 

#part 4: dynamic programming the fast way for each note and each finger- remember only the 
#cheapest way to get there 
def best_fingering(notes): 
    fingers = [1, 2, 3, 4, 5]
    cost= [{f: (1 if f == 1 and is_black(notes[0]) else 0) for f in fingers}]
    came_from = [{}]

    for i in range(1, len(notes)): 
        cost.append({})
        came_from.apend({})
        for f in fingers: 
            #try every finger on the previous note, keep the cheapest
            options = {}
            for prev in fingers: 
                options[prev] = cost[i - 1][prev] + move_cost(notes[ i -1 ], prev, notes[i], f)
                best_prev = min(options, key= options.get)
                cost[i][f] = options[best_prev]
                came_from[i][f] = best_prev 

    #start at the cheapest last finger and walk back 
    f = min(cost[-1], key=cost[-1].get)
    fingering = [f]
    for i in range (len(notes) - 1, 0, -1): 
        f = came_from[i][f]
        fingering.append(f)
    fingering.reverse()
    return fingering, min(cost[-1].values())

#final touch - read the melodies and print the fingering under the notes 
def main(): 
    with open("melodies.txt") as file: 
        for line in file:
            if not line.strip() or line.startswith("#"): 
                continue 
            name, text = line.split(":", 1)
            names = text.split()
            notes = [to_midi(n) for n in names]
            fingering, cost = best_fingering(notes)

            print(f"{name.strip()} (cost {cost})")
            print(" " + " ".join(f"{n:>4}" for n in names))
            print(" " + " ".join(f"{f:>4}" for f in fingering))
            if len(notes) <= 8: 
                _, bf_cost = brute_force(notes)
                print(" brute force agrees" if bf_cost == cost else f"  brute force: cost {bf_cost}")
            print()

if __name__ == "__main__": 
    main()