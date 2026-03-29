#!/usr/bin/env python3
import argparse
import csv
import random

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', default='project_seed_dataset.csv')
    ap.add_argument('--rows', type=int, default=3000)
    ap.add_argument('--seed', type=int, default=42)
    args = ap.parse_args()

    random.seed(args.seed)
    with open(args.output, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['timestamp_ms','avg_temp','avg_humi','label_hot','source'])
        for i in range(args.rows):
            temp = random.uniform(23.5, 37.5)
            hum = random.uniform(45, 95)
            discomfort = 0.58*(temp-29.5) + 0.042*(hum-70) + 0.018*(temp-29.5)*(hum-70)
            label = 1 if discomfort > 1.0 else 0
            if temp >= 31 and hum >= 75:
                label = 1
            if temp <= 27 and hum <= 70:
                label = 0
            if random.random() < 0.04:
                label = 1 - label
            w.writerow([i*2000, round(temp,3), round(hum,3), label, 'seed_south_vn'])

if __name__ == '__main__':
    main()
