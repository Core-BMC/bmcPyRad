import os
import glob
import csv
import subprocess
from tqdm import tqdm
from itertools import product


class RadiomicsPreparation:
    def __init__(self, folder_path, n=100):
        self.folder_path = os.path.abspath(folder_path)
        self.n = n
        # Include all case variations for the types
        self.types = [
            "RTF", "RTM", "RCF", "RCM"
        ]
        self.sides = ["Right", "Left"]
        self.input_file = "input_all_types.csv"

    def prepare_input_file(self):
        """
        Search the given folder for files of type 'RTF', 'RCF', 'RTM', 'RCM'
        and sides 'Right', 'Left' with various case combinations, and create
        an input_all_types.csv file.
        Only actual existing files will be used.
        """
        with open(self.input_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Image", "Mask"])

            # Show the progress bar for the overall process
            total_iterations = len(self.types) * len(self.sides) * self.n
            progress_bar = tqdm(total=total_iterations,
                                desc="Creating CSV file")

            # Loop through each type and side combination
            for type_name, side in product(self.types, self.sides):
                # Loop from 1 to the given n value
                for i in range(1, self.n + 1):
                    # Format i to match the patient number
                    formatted_i = f"{i}"

                    # Define possible patterns to handle various file name styles
                    patterns = [
                        f"{type_name}{formatted_i}_{side}30x30x30.nii",
                        f"{type_name}_{formatted_i}_{side}30x30x30.nii"
                    ]

                    # Use glob to find files matching any of the patterns
                    image_path = None
                    for pattern in patterns:
                        found_images = glob.glob(os.path.join(self.folder_path, "**", pattern), recursive=True)
                        found_images = list(set(found_images))  # Remove duplicates
                        # Check if the found image path exists and is a file
                        if found_images:
                            for img_path in found_images:
                                if os.path.isfile(img_path):
                                    image_path = os.path.abspath(img_path)
                                    break
                        if image_path:
                            break

                    # If no image file is found, skip to the next iteration
                    if not image_path:
                        continue

                    # Define possible patterns for masks
                    mask_patterns = {
                        "all": [
                            f"{type_name}{formatted_i}_{side}_cropped_all.nii",
                            f"{type_name}_{formatted_i}_{side}_cropped_all.nii"
                        ],
                        "bone": [
                            f"{type_name}{formatted_i}_{side}_cropped_bone.nii",
                            f"{type_name}_{formatted_i}_{side}_cropped_bone.nii"
                        ]
                    }

                    # Find the first matching mask for each type (all, bone)
                    mask_all_path = None
                    mask_bone_path = None

                    for pattern in mask_patterns["all"]:
                        found_masks = glob.glob(os.path.join(self.folder_path, "**", pattern), recursive=True)
                        found_masks = list(set(found_masks))  # Remove duplicates
                        for mask_path in found_masks:
                            if os.path.isfile(mask_path):
                                mask_all_path = os.path.abspath(mask_path)
                                break
                        if mask_all_path:
                            break

                    for pattern in mask_patterns["bone"]:
                        found_masks = glob.glob(os.path.join(self.folder_path, "**", pattern), recursive=True)
                        found_masks = list(set(found_masks))  # Remove duplicates
                        for mask_path in found_masks:
                            if os.path.isfile(mask_path):
                                mask_bone_path = os.path.abspath(mask_path)
                                break
                        if mask_bone_path:
                            break

                    # If both image and first mask exist, add to CSV
                    if image_path and mask_all_path:
                        writer.writerow([
                            f"all_{side}_{type_name}_{formatted_i}",
                            image_path, mask_all_path
                        ])
                        print(f"Written to CSV: all_{side}_{type_name}_{formatted_i}, {image_path}, {mask_all_path}")

                    # If both image and second mask exist, add to CSV
                    if image_path and mask_bone_path:
                        writer.writerow([
                            f"bone_{side}_{type_name}_{formatted_i}",
                            image_path, mask_bone_path
                        ])
                        print(f"Written to CSV: bone_{side}_{type_name}_{formatted_i}, {image_path}, {mask_bone_path}")

                    # Update the progress bar
                    progress_bar.update(1)

            # Close the progress bar when done
            progress_bar.close()

        print(f"CSV file has been created: {self.input_file}")

    def run_pyradiomics(self, output_file, format="csv", jobs=3,
                        skip_nans=True):
        """
        Run Pyradiomics to extract radiomic features.
        Args:
            output_file (str): The name of the output file.
            format (str): The output format (default: csv).
            jobs (int): Number of cores to use (default: 3).
            skip_nans (bool): Whether to skip NaNs (default: True).
        """
        command = [
            "pyradiomics",
            self.input_file,
            "-o", output_file,
            "-f", format,
            "-j", str(jobs)
        ]

        if skip_nans:
            command.append("--skip-nans")

        print("Running command: ", " ".join(command))

        try:
            subprocess.run(command, check=True)
            print(f"Pyradiomics has completed: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error during Pyradiomics execution: {e}")
        except FileNotFoundError:
            print("Pyradiomics is not installed or the path is incorrect.")


# Example usage
if __name__ == "__main__":
    # Set the folder path and n value
    folder_path = "./TMJOA"
    n = 34  # Change the n value if needed.

    # Create an instance of the RadiomicsPreparation class
    radiomics_prep = RadiomicsPreparation(folder_path, n)

    # Prepare the input file
    radiomics_prep.prepare_input_file()

    # Run Pyradiomics
    output_file = "output_features_TMJOA.csv"
    radiomics_prep.run_pyradiomics(output_file)
