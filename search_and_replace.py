# =======================================================================
# Copyright 2025 UCLA NanoCAD Laboratory
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =======================================================================

# Read command line arguments
import sys

if len(sys.argv) != 5:
    print("Usage: python script.py input_file string_to_replace replacement_string output_file")
    sys.exit(1)

input_file, string_to_replace, replacement_string, output_file = sys.argv[1:]

# Read input file
try:
    with open(input_file, 'r') as fin:
        content = fin.read()
except FileNotFoundError:
    print(f"Input file '{input_file}' not found.")
    sys.exit(1)

# Replace occurrences
new_content = content.replace(string_to_replace, replacement_string)

# Write to output file
with open(output_file, 'w') as fout:
    fout.write(new_content)

# print(f"Replaced '{string_to_replace}' with '{replacement_string}' in '{input_file}'. Result saved in '{output_file}'.")

