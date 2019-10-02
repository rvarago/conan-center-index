from conans import ConanFile, CMake, tools
import os.path


class AbsentConan(ConanFile):
    name = "absent"
    description = "A simple library to compose nullable types in a generic, type-safe, and declarative style for C++"
    homepage = "https://github.com/rvarago/absent"
    url = "https://github.com/conan-io/conan-center-index"
    license = "MIT"
    author = "Rafael Varago (rvarago)"
    topics = ("nullable-types", "composition", "monadic-interface", "declarative-programming")
    no_copy_source = True
    generators = "cmake"

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTS"] = "OFF"
        cmake.configure(source_folder=self._source_subfolder,
                        build_folder=self._build_subfolder)
        return cmake

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))

    def package_id(self):
        self.info.header_only()