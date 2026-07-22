# Logistics Route Optimization & Freight Cost Engine

## Overview
This project models multi-city transport efficiency, computes haul distances via vectorized Haversine geometry, calculates freight cost structures, and analyzes lane payload consolidation across 500 shipment records.

## Core Metrics & Methodology
- **Haversine Distance:** Calculates exact great-circle distance between coordinate pairs (origin and destination hubs).
- **Freight Cost Model:** Applies base rates, distance fees (€1.20/km), weight charges (€0.05/kg), and a 12% fuel surcharge.
- **Cost per Ton-KM:** Standardizes transport financial expenditure per payload unit moved over distance.
- **Lane Consolidation:** Aggregates shipments by origin-destination corridors and estimates 24-ton full truckload (FTL) requirements for LTL optimization.

## Repository Structure
- `generate_route_data.py`: Multi-city European shipment dataset generator.
- `shipments.csv`: Raw dataset containing 500 shipment orders and coordinates.
- `optimize_routes.py`: Python routing and cost optimization engine.
- `optimized_freight_routes.xlsx`: Multi-tab workbook with shipment calculations and lane consolidation summaries.
- `freight_efficiency_distribution.png`: Auto-generated distribution plot of cost per Ton-KM.

## How to Run
```cmd
python optimize_routes.py