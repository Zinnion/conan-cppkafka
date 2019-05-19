#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os

class CppKafkaConan(ConanFile):
    name = "cppkafka"
    version = "0.3.1"
    description = "Modern C++ Apache Kafka client library (wrapper for librdkafka)"
    topics = ("conan", "librdkafka")
    url = "https://github.com/zinnion/conan-cppkafka"
    homepage = "https://github.com/mfontanini/cppkafka"
    author = "Zinnion <mauro@zinnion.com>"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    settings = "os", "compiler", "build_type", "arch"
    short_paths = True
    generators = "cmake"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    options = {
       "shared": [True, False],
       "static": [True, False],
       "multithreaded": [True, False]
    }

    default_options = (
        "shared=False",
        "static=True",
        "multithreaded=True",
    )

    def source(self):
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def requirements(self):
        self.requires.add("boost/1.70.0@zinnion/stable")
        self.requires.add("librdkafka/1.0.0@zinnion/stable")

    def configure(self):
        del self.settings.compiler.libcxx
        if self.settings.compiler == "Visual Studio" and float(self.settings.compiler.version.value) < 14:
            raise Exception("ngg could not be built by MSVC <14")

    def configure_cmake(self):
        cmake = CMake(self)
        opts = dict()
        opts["RDKAFKA_LIBRARY"] = self.deps_cpp_info["librdkafka"].rootpath
        opts["RDKAFKA_INCLUDE_DIR"] = self.deps_cpp_info["librdkafka"].rootpath + "/include"
        cmake.definitions["CPPKAFKA_BUILD_SHARED"] = self.options.shared
        cmake.definitions["CPPKAFKA_BOOST_USE_MULTITHREADED"] = self.options.multithreaded
        cmake.definitions["CPPKAFKA_RDKAFKA_STATIC_LIB"] = self.options.static
        cmake.configure(defs=opts, source_folder=self.source_subfolder, build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE.txt", dst="license", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Windows":
            if not self.options.shared:
                self.cpp_info.libs.append('mswsock')
                self.cpp_info.libs.append('ws2_32')
        elif self.settings.os == "Linux":
            self.cpp_info.libs.append('pthread')
        #if not self.options.shared:
        #    self.cpp_info.defines.append("CPPKAFKA_RDKAFKA_STATIC_LIB")
