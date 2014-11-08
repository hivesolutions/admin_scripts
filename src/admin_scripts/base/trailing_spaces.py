#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Administration Scripts
# Copyright (c) 2008-2014 Hive Solutions Lda.
#
# This file is part of Hive Administration Scripts.
#
# Hive Administration Scripts is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Administration Scripts is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Administration Scripts. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import sys
import getopt

import legacy

USAGE_MESSAGE = "remove-trailing-spaces-python path [-r] [-t] [-n] [-u] [-e file_extension_1, file_extension_2, ...] [-w exclusion_1, exclusion_2, ...] [-c configuration_file]"
""" The usage message """

SPACE_TAB = b"    "
""" The space tab string """

RELATIVE_BASE_PATH = "/.."
""" The relative base path """

LONG_PATH_PREFIX = legacy.UNICODE("\\\\?\\")
""" The windows long path prefix """

NT_PLATFORM_VALUE = "nt"
""" The nt platform value """

DOS_PLATFORM_VALUE = "dos"
""" The dos platform value """

WINDOWS_PLATFORMS_VALUE = (
    NT_PLATFORM_VALUE,
    DOS_PLATFORM_VALUE
)
""" The windows platform value """

def normalize_path(path):
    """
    Normalizes the given path, using the characteristics
    of the current environment.
    In windows this function adds support for long path names.

    @type path: String
    @param path: The path to be normalized.
    @rtype: String
    @return: The normalized path.
    """

    # retrieves the current os name
    os_name = os.name

    # in case the current operative system is windows based and
    # the normalized path does start with the long path prefix it
    # must be removed to allow a "normal" path normalization
    if os_name in WINDOWS_PLATFORMS_VALUE and path.startswith(LONG_PATH_PREFIX):
        # removes the long path prefix from the path
        path = path[4:]

    # checks if the path is absolute
    is_absolute_path = os.path.isabs(path)

    # in case the path is not absolute (creates problem in windows
    # long path support)
    if os_name in WINDOWS_PLATFORMS_VALUE and not is_absolute_path:
        # converts the path to absolute
        path = os.path.abspath(path)

    # normalizes the path
    normalized_path = os.path.normpath(path)

    # in case the current operative system is windows based and
    # the normalized path does not start with the long path prefix
    if os_name in WINDOWS_PLATFORMS_VALUE and not normalized_path.startswith(LONG_PATH_PREFIX):
        # creates the path in the windows mode, adds
        # the support for long path names with the prefix token
        normalized_path = LONG_PATH_PREFIX + normalized_path

    # returns the normalized path
    return normalized_path

def remove_trailing_newlines(file_path, windows_newline = True):
    """
    Removes the extra newlines in the file with the given
    file path.
    The extra argument defines if the newline format used
    should be the windows mode (carriage return and newline).

    @type file_path: String
    @param file_path: The path to the file to have the trailing
    newlines removed.
    @type windows_newline: bool
    @param windows_newline: If the windows newline should be used.
    """

    # normalizes the file path
    file_path_normalized = normalize_path(file_path)

    # opens the file for reading
    file = open(file_path_normalized, "rb")

    try:
        # creates a string buffer for buffering
        string_buffer = legacy.BytesIO()

        # reads the file lines
        file_lines = file.readlines()

        # reverses the file lines
        file_lines.reverse()

        # start the index
        index = 0

        # iterates over all the lines in the file
        for line in file_lines:
            # in case the line is not just a newline character
            if not line == b"\n" and not line == b"\r\n":
                # breaks the cycle
                break

            # decrements the index
            index -= 1

        # reverses the file lines
        file_lines.reverse()

        if index == 0:
            # retrieves the valid file lines
            valid_file_lines = file_lines
        else:
            # retrieves the valid file lines
            valid_file_lines = file_lines[:index]

        # iterates over all the file lines
        for valid_file_line in valid_file_lines:
            # strips the valid file line
            valid_file_line_stripped = valid_file_line.rstrip()

            # writes the valid file line stripped to the string buffer
            string_buffer.write(valid_file_line_stripped)

            # in case the newline mode is of type windows
            if windows_newline:
                # writes the carriage return character and the new line character
                string_buffer.write(b"\r\n")
            else:
                # writes the new line character
                string_buffer.write(b"\n")
    finally:
        # closes the file for reading
        file.close()

    # retrieves the string value from the string buffer
    string_value = string_buffer.getvalue()

    # opens the file for writing and outputs the complete
    # set of normalized generated contents into it
    file = open(file_path_normalized, "wb")
    try: file.write(string_value)
    finally: file.close()

def remove_trailing_spaces(file_path, tab_to_spaces, windows_newline = True):
    """
    Removes the extra spaces or tabs in every line of the
    file contents.
    The extra argument defines if the newline format used
    should be the windows mode (carriage return and newline).

    @type file_path: String
    @param file_path: The path to the file to have the trailing
    spaces removed.
    @type tab_to_spaces: bool
    @param tab_to_spaces: If the tab characters should be converted
    to spaces.
    @type windows_newline: bool
    @param windows_newline: If the windows newline should be used.
    """

    # normalizes the file path
    file_path_normalized = normalize_path(file_path)

    # opens the file for reading
    file = open(file_path_normalized, "rb")

    try:
        # creates a string buffer for buffering
        string_buffer = legacy.BytesIO()

        # iterates over all the lines in the file
        for line in file:
            # strips the line
            line_stripped = line.rstrip()

            # in case the tab must be replaced with spaces
            # performs the operations with the proper way
            if tab_to_spaces:
                line_stripped = line_stripped.replace(b"\t", SPACE_TAB)

            # writes the stripped line to the string buffer
            string_buffer.write(line_stripped)

            # writes the proper line ending sequence taking into
            # account if the windows newline should be used or not
            if windows_newline: string_buffer.write(b"\r\n")
            else: string_buffer.write(b"\n")
    finally:
        # closes the file for reading
        file.close()

    # retrieves the string value from the string buffer
    # this should be a bytes based buffer string
    string_value = string_buffer.getvalue()

    # opens the file for writing and writes the complete
    # set of generated contents into it (output operation)
    file = open(file_path_normalized, "wb")
    try: file.write(string_value)
    finally: file.close()

def remove_trailing_spaces_walker(arguments, directory_name, names):
    """
    Walker method to be used by the path walker for the removal of trailing
    spaces and newlines.

    @type arguments: Tuple
    @param arguments: The arguments tuple sent by the walker method.
    @type directory_name: String
    @param directory_name: The name of the current directory in the walk.
    @type names: List
    @param names: The list of names in the current directory.
    """

    # unpacks the arguments tuple
    tab_to_spaces, trailing_newlines, windows_newline,\
    file_extensions, file_exclusion = arguments

    # removes the complete set of names that are meant to be excluded from the
    # current set names to be visit (avoid visiting them)
    for exclusion in file_exclusion:
        if not exclusion in names: continue
        names.remove(exclusion)

    # retrieves the valid names for the names list (removes directory entries)
    valid_complete_names = [
        directory_name + "/" + name for name in names\
        if not os.path.isdir(directory_name + "/" + name)
    ]

    # filters the names with non valid file extensions
    valid_complete_names = [
        os.path.normpath(name) for name in valid_complete_names\
        if file_extensions == None or name.split(".")[-1] in file_extensions
    ]

    # iterates over all the valid complete names with extension filter
    for valid_complete_name in valid_complete_names:
        # print a message
        print("Removing trail in file: %s" % valid_complete_name)

        # removes the trailing spaces for the (path) name
        remove_trailing_spaces(valid_complete_name, tab_to_spaces, windows_newline)

        # in case the trailing newlines flag is active
        if trailing_newlines:
            # prints a message
            print("Removing trail newlines in file: %s" % (valid_complete_name,))

            # removes the trailing newlines for the(path) name
            remove_trailing_newlines(valid_complete_name, windows_newline)

def remove_trailing_spaces_recursive(
    directory_path,
    tab_to_spaces,
    trailing_newlines,
    windows_newline,
    file_extensions = None,
    file_exclusion = None
):
    """
    Removes the trailing spaces in recursive mode.
    All the options are arguments to be passed to the
    walker function.

    @type directory_path: String
    @param directory_path: The path to the (entry point) directory.
    @type tab_to_spaces: bool
    @param tab_to_spaces: If the tab characters should be converted
    to spaces.
    @type trailing_newlines: bool
    @param trailing_newlines: If the trailing newline characters should be removed.
    @type windows_newline: bool
    @param windows_newline: If the windows newline should be used.
    @type file_extensions: List
    @param file_extensions: The list of file extensions to be used.
    @type file_exclusion: List
    @param file_exclusion: The list of file exclusion to be used.
    """

    legacy.walk(
        directory_path,
        remove_trailing_spaces_walker,
        (
            tab_to_spaces,
            trailing_newlines,
            windows_newline,
            file_extensions,
            file_exclusion
        )
    )

def _retrieve_configurations(
    recursive,
    tab_to_spaces,
    trailing_newlines,
    windows_newline,
    file_extensions,
    file_exclusion,
    configuration_file_path
):
    """
    Retrieves the configuration maps for the given arguments.

    @type recursive: bool
    @param recursive: If the removing should be recursive.
    @type tab_to_spaces: bool
    @param tab_to_spaces: If the tab characters should be converted
    to spaces.
    @type trailing_newlines: bool
    @param trailing_newlines: If the trailing newline characters should be removed.
    @type windows_newline: bool
    @param windows_newline: If the windows newline should be used.
    @type file_extensions: List
    @param file_extensions: The list of file extensions to be used.
    @type file_exclusion: List
    @param file_exclusion: The list of file exclusion to be used.
    @type configuration_file_path: String
    @param configuration_file_path: The path to the configuration file.
    """

    # in case the configuration file path is defined
    if configuration_file_path:
        # creates the base path from the file paths
        base_path = os.path.dirname(os.path.realpath(__file__)) + RELATIVE_BASE_PATH

        # retrieves the real base path
        real_base_path = os.path.realpath(base_path)

        # retrieves the configuration directory from the configuration
        # file path (the directory is going to be used to include the module)
        configuration_directory_path = os.path.dirname(configuration_file_path)

        # in case the configuration directory path is not an absolute path
        if not os.path.isabs(configuration_directory_path):
            # creates the (complete) configuration directory path prepending the manager path
            configuration_directory_path = real_base_path + "/" + configuration_directory_path

        # in case the configuration directory path is valid inserts it into the system path
        configuration_directory_path and sys.path.insert(0, configuration_directory_path)

        # retrieves the configuration file base path from the configuration file path
        configuration_file_base_path = os.path.basename(configuration_file_path)

        # retrieves the configuration module name and the configuration module extension by splitting the
        # configuration base path into base name and extension
        configuration_module_name, _configuration_module_extension = os.path.splitext(configuration_file_base_path)

        # imports the configuration module
        configuration = __import__(configuration_module_name)

        # retrieves the configurations from the configuration module
        configurations = configuration.configurations
    else:
        # creates the base configuration map
        base_configuration = {}

        # sets the base configuration map attributes
        base_configuration["recursive"] = recursive
        base_configuration["tab_to_spaces"] = tab_to_spaces
        base_configuration["trailing_newlines"] = trailing_newlines
        base_configuration["windows_newline"] = windows_newline
        base_configuration["file_extensions"] = file_extensions
        base_configuration["file_exclusion"] = file_exclusion

        # creates the configurations tuple with the base configurations
        configurations = (
            base_configuration,
        )

    # returns the configurations tuple
    return configurations

def main():
    """
    Main function used for the removal of both the trailing spaces
    and the extra newlines.
    """

    # in case the number of arguments
    # is not sufficient
    if len(sys.argv) < 2:
        # prints a message
        print("Invalid number of arguments")

        # prints the usage message
        print("Usage: " + USAGE_MESSAGE)

        # exits the system in error
        sys.exit(2)

    # sets the default values for the parameters
    path = sys.argv[1]
    recursive = False
    tab_to_spaces = False
    trailing_newlines = False
    windows_newline = True
    file_extensions = None
    file_exclusion = None
    configuration_file_path = None

    try:
        options, _arguments = getopt.getopt(sys.argv[2:], "rtnue:c:", [])
    except getopt.GetoptError:
        # prints a message
        print("Invalid number of arguments")

        # prints the usage message
        print("Usage: " + USAGE_MESSAGE)

        # exits the system in error
        sys.exit(2)

    # iterates over all the options, retrieving the option
    # and the value for each
    for option, value in options:
        if option == "-r":
            recursive = True
        elif option == "-t":
            tab_to_spaces = True
        elif option == "-n":
            trailing_newlines = True
        elif option == "-u":
            windows_newline = False
        elif option == "-e":
            file_extensions = [value.strip() for value in value.split(",")]
        elif option == "-w":
            file_exclusion = [value.strip() for value in value.split(",")]
        elif option == "-c":
            configuration_file_path = value

    # retrieves the configurations from the command line arguments
    configurations = _retrieve_configurations(
        recursive,
        tab_to_spaces,
        trailing_newlines,
        windows_newline,
        file_extensions,
        file_exclusion,
        configuration_file_path
    )

    # iterates over all the configurations, executing them
    for configuration in configurations:
        # retrieves the configuration values
        recursive = configuration["recursive"]
        tab_to_spaces = configuration["tab_to_spaces"]
        trailing_newlines = configuration["trailing_newlines"]
        windows_newline = configuration["windows_newline"]
        file_extensions = configuration["file_extensions"] or ()
        file_exclusion = configuration["file_exclusion"] or ()

        # in case the recursive flag is set
        if recursive:
            # removes the trailing spaces in recursive mode
            remove_trailing_spaces_recursive(
                path,
                tab_to_spaces,
                trailing_newlines,
                windows_newline,
                file_extensions,
                file_exclusion
            )
        # otherwise it's a "normal" iteration
        else:
            # removes the trailing spaces (for one file)
            remove_trailing_spaces(path, tab_to_spaces, windows_newline)

            # in case the trailing newlines
            if trailing_newlines:
                # removes the trailing newlines (for one file)
                remove_trailing_newlines(path, windows_newline)

if __name__ == "__main__":
    main()