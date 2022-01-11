#!/bin/bash

ups -pg a4 -f examples/ups_a4_landscape.svg
ups -pg a4 -p -f examples/ups_a4_portrait.svg

ups -pg letter -f examples/ups_letter_landscape.svg
ups -pg letter -p -f examples/ups_letter_portrait.svg