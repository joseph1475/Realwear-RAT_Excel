# /*
#  * RealWear Development Software, Source Code and Object Code.
#  * (c) RealWear, Inc. All rights reserved.
#  *
#  * Contact info@realwear.com for further information about the use of this code.
#  */
from requests.packages import package
import com
import android

package com.realwear.systemeventservice

import android.app.UiAutomation
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import androidx.test.core.app.ApplicationProvider
import androidx.test.platform.app.InstrumentationRegistry
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.uiautomator.By
import androidx.test.uiautomator.Configurator
import androidx.test.uiautomator.UiDevice
import androidx.test.uiautomator.Until
import com.realwear.systemeventservicelib.RealWearAccessibilityService
import com.realwear.systemeventservicelib.RealWearSystemEvent
import com.realwear.systemeventservicelib.RealWearSystemEventListener
import org.awaitility.Awaitility

import org.junit.runner.RunWith

import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import java.util.concurrent.TimeUnit

/**
 * Tests for detecting the notification draw opening and closing.
 */
@RunWith(AndroidJUnit4::class)
class NotificationDrawTest {
    private var uiDevice: UiDevice? = null

    private val eventListener = RealWearAccessibilityServiceListener()

    @Before
    fun setupSystemEventService() {
        //
        // Enable on System Event Service in Android Settings.
        //
        val packageName = "com.realwear.systemeventservice"
        val className = "com.realwear.systemeventservicelib.RealWearAccessibilityService"
        val cmd = "settings put secure enabled_accessibility_services $packageName/$className"
        InstrumentationRegistry
            .getInstrumentation()
            .getUiAutomation(UiAutomation.FLAG_DONT_SUPPRESS_ACCESSIBILITY_SERVICES)
            .executeShellCommand(cmd)
            .close()

        //
        // Set up UiAutomation device. We need to make sure that it doesn't block accessibility
        // services though, otherwise System Event Service doesn't get any accessibility events.
        //
        Configurator.getInstance().uiAutomationFlags =
            UiAutomation.FLAG_DONT_SUPPRESS_ACCESSIBILITY_SERVICES
        uiDevice = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation())

        setScreenPowerState(Power.On)
        navigateHome()

        RealWearAccessibilityService.listener = eventListener
        eventListener.events.clear()
        assertTrue(eventListener.events.isEmpty())
    }