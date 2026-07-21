plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
    id("org.jlleitschuh.gradle.ktlint")
}

android {
    namespace = "com.pampan.pampan"
    compileSdk = 36
    buildToolsVersion = "36.0.0"

    defaultConfig {
        applicationId = "com.pampan.pampan"
        minSdk = 26
        targetSdk = 36
        versionCode = 1
        versionName = "0.1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
    buildFeatures {
        compose = true
        buildConfig = false
    }
    packaging {
        resources.excludes += "/META-INF/{AL2.0,LGPL2.1}"
    }
}

dependencies {
    implementation(platform("androidx.compose:compose-bom:2025.05.01"))
    androidTestImplementation(platform("androidx.compose:compose-bom:2025.05.01"))

    implementation("androidx.activity:activity-compose:1.10.1")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-tooling-preview")

    debugImplementation("androidx.compose.ui:ui-tooling")
    debugImplementation("androidx.compose.ui:ui-test-manifest")

    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.2.1")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.6.1")
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")
}

ktlint {
    version.set("1.5.0")
    android.set(true)
}

dependencyLocking {
    lockAllConfigurations()
}

val releaseRuntimeLock = layout.projectDirectory.file("runtime-dependencies/gradle.lockfile")

tasks.register("writeReleaseRuntimeLock") {
    group = "verification"
    description = "Exports the resolved shipped release runtime graph for OSV scanning."
    outputs.file(releaseRuntimeLock)

    doLast {
        val coordinates =
            configurations
                .getByName("releaseRuntimeClasspath")
                .resolvedConfiguration
                .resolvedArtifacts
                .map { artifact ->
                    val module = artifact.moduleVersion.id
                    "${module.group}:${module.name}:${module.version}=releaseRuntimeClasspath"
                }.distinct()
                .sorted()

        require(coordinates.isNotEmpty()) {
            "Resolved release runtime dependency graph must not be empty."
        }

        val output = releaseRuntimeLock.asFile
        output.parentFile.mkdirs()
        output.writeText(
            "# Generated from Gradle's resolved releaseRuntimeClasspath.\n" +
                "# Regenerate with :app:writeReleaseRuntimeLock.\n" +
                coordinates.joinToString(separator = "\n", postfix = "\n"),
        )
    }
}
