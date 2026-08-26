# Copyright © 2023 CCP ehf.

project(TrinityALTest VERSION 1.0.0)

set(_SOURCES 
    ALResultTest.cpp
    BitmapDimensions.cpp
    Buffer.cpp
    Compute.cpp
    ConstantBuffer.cpp
    DepthStencil.cpp
    Dxt1Image.h
    Dxt3Image.h
    Dxt5Image.h
    Dxt5Volume.h
    FakeGoogleTest.h
    Fence.cpp
    GPUTimer.cpp
    OcclusionQuery.cpp
    Raytracing.cpp
    RenderContext.cpp
    RenderContextCreation.cpp
    RenderTarget.cpp
    RenderWindow.h
    RenderWindow_Stub.cpp
    RenderWindow_Win32.cpp
    RenderWindow_Macos.mm
    Rendering.cpp
    SamplerState.cpp
    Shader.cpp
    StdAfx.h
    StdAfx.cpp
    SwapChain.cpp
    SwapChainResizing.cpp
    Texture.cpp
    TextureSubresource.cpp
    TrinityALTest.cpp
    VertexDefinition.cpp
    VertexLayout.cpp
    VideoAdapterInfo.cpp
    WithRenderContextFixture.h
    WithRenderContextFixture.cpp
    WithValidRenderContextFixture.h
    WithValidRenderContextFixture.cpp
    WithWindowFixture.h
    WithWindowFixture_Stub.cpp
    WithWindowFixture_Win32.cpp
    WithWindowFixture_Macos.mm
    XrgbVolume.h
)

set(_SHADERS_DX11
    Shaders.DX11/AddConstantToBuffer.csh
    Shaders.DX11/AddVectors.csh
    Shaders.DX11/ConstantColor.psh
    Shaders.DX11/GroupShared.csh
    Shaders.DX11/InstancedRendering.vsh
    Shaders.DX11/LoadMsaaTexture.psh
    Shaders.DX11/OutputTexCoord.psh
    Shaders.DX11/OutputVector.csh
    Shaders.DX11/PositionOnly.vsh
    Shaders.DX11/PositionOnlyWithPerObjectData.vsh
    Shaders.DX11/SampleTexture.csh
    Shaders.DX11/SampleTextureFromTexCoord.psh
    Shaders.DX11/SampleTextureMipFromTexCoord.psh
    Shaders.DX11/SampleVolumeTexture.psh
    Shaders.DX11/TexCoordAndPosition.vsh
    Shaders.DX11/WriteToUav.psh
)

set(_SHADERS_DX12
    Shaders.DX12/AddConstantToBuffer.csh
    Shaders.DX12/AddVectors.csh
    Shaders.DX12/ClosestHit.rsh
    Shaders.DX12/ClosestHitWithMaterial.rsh
    Shaders.DX12/ConstantColor.psh
    Shaders.DX12/GroupShared.csh
    Shaders.DX12/InstancedRendering.vsh
    Shaders.DX12/LoadMsaaTexture.psh
    Shaders.DX12/Miss.rsh
    Shaders.DX12/OutputTexCoord.psh
    Shaders.DX12/OutputVector.csh
    Shaders.DX12/PositionOnly.vsh
    Shaders.DX12/PositionOnlyWithPerObjectData.vsh
    Shaders.DX12/RayGen.rsh
    Shaders.DX12/SampleTexture.csh
    Shaders.DX12/SampleTextureFromTexCoord.psh
    Shaders.DX12/SampleTextureMipFromTexCoord.psh
    Shaders.DX12/SampleVolumeTexture.psh
    Shaders.DX12/TexCoordAndPosition.vsh
    Shaders.DX12/WriteToUav.psh
)

set(_SHADERS_METAL
    Shaders.metal/AddConstantToBuffer.csh
    Shaders.metal/AddVectors.csh
    Shaders.metal/ClosestHit.rsh
    Shaders.metal/ClosestHitWithMaterial.rsh
    Shaders.metal/ConstantColor.psh
    Shaders.metal/GroupShared.csh
    Shaders.metal/InstancedRendering.vsh
    Shaders.metal/LoadMsaaTexture.psh
    Shaders.metal/MetalDefines.h
    Shaders.metal/Miss.rsh
    Shaders.metal/OutputTexCoord.psh
    Shaders.metal/OutputVector.csh
    Shaders.metal/PositionOnly.vsh
    Shaders.metal/PositionOnlyWithPerObjectData.vsh
    Shaders.metal/RayGen.rsh
    Shaders.metal/SampleTexture.csh
    Shaders.metal/SampleTextureFromTexCoord.psh
    Shaders.metal/SampleTextureMipFromTexCoord.psh
    Shaders.metal/SampleVolumeTexture.psh
    Shaders.metal/TexCoordAndPosition.vsh
    Shaders.metal/WriteToUav.psh
)

set(GENERATED_SOURCES_DIR ${CMAKE_CURRENT_BINARY_DIR}/GeneratedSources)

find_package(GTest CONFIG REQUIRED)

function(set_shared_trinityaltest_properties target)

    target_include_directories(${target}
        PRIVATE
            ${CMAKE_CURRENT_SOURCE_DIR}
            ${CMAKE_CURRENT_SOURCE_DIR}/..
    )

    target_compile_definitions(${target} PRIVATE TRINITY_AL_WITH_BLUE_EXPOSURE=0 BLUEBUILD)
    target_precompile_headers(${target} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/StdAfx.h)

    if(BUILD_FOR_PYTHON_2)
        target_link_libraries(${target} PRIVATE GTest::GTest GTest::Main)
    else()
        target_link_libraries(${target} PRIVATE GTest::gtest GTest::gtest_main GTest::gmock GTest::gmock_main)
    endif()
    
    if(APPLE)
        file(GLOB_RECURSE _CPP_SOURCES "*.cpp")
        set_source_files_properties(${_CPP_SOURCES} PROPERTIES LANGUAGE OBJCXX)
        target_compile_options(${target} PRIVATE "-fobjc-arc")
        set_target_properties(${target} PROPERTIES LINKER_LANGUAGE OBJCXX)

        target_link_libraries(${target} PRIVATE "-framework CoreFoundation")
        target_link_libraries(${target} PRIVATE "-framework Cocoa")
    elseif(WIN32)
        target_link_options(${target} PRIVATE "/IGNORE:4049")
    endif()

    target_include_directories(${target} PRIVATE ${GENERATED_SOURCES_DIR})

    # override the output directory to ensure that all TrinityALTest outputs end up in the same folder.
    # this is OK because we're differentiating them by OUTPUT_NAME
    set(output_directory "${CMAKE_BINARY_DIR}/carbon/autobuild/TrinityALTest/${CCP_PLATFORM}/${CCP_ARCHITECTURE}/${CCP_TOOLSET}/$<$<CONFIG:DEBUG>:>")
    message(STATUS "Overriding ${target} output directory to ${output_directory}")
    set_target_properties(${target}
        PROPERTIES
            RUNTIME_OUTPUT_DIRECTORY ${output_directory}
            PDB_OUTPUT_DIRECTORY ${output_directory}
            FOLDER Trinity/Tests
    )

endfunction()

if(WIN32)
    if (BUILD_DX11)
        ccp_add_executable(TrinityALTest_dx11 ${_SOURCES})
        target_link_libraries(TrinityALTest_dx11 PRIVATE TrinityAL_dx11)
        target_compile_definitions(TrinityALTest_dx11 PRIVATE TRINITY_PLATFORM=TRINITY_DIRECTX11)
        set_shared_trinityaltest_properties(TrinityALTest_dx11)

        #GTest
        set_target_properties(TrinityALTest_dx11 PROPERTIES FOLDER "Tests")
        #gtest_discover_tests(TrinityALTest_dx11 myListOfTests)

        # Copy DLL dependencies
        add_custom_command(
            TARGET TrinityALTest_dx11 POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy_if_different $<TARGET_RUNTIME_DLLS:TrinityALTest_dx11> $<TARGET_FILE_DIR:TrinityALTest_dx11>
            COMMAND_EXPAND_LISTS
        )

        target_sources(TrinityALTest_dx11 PRIVATE ${_SHADERS_DX11})
        source_group(Shaders FILES ${_SHADERS_DX11})

        if(BUILD_FOR_PYTHON_2)
            find_package(fxc CONFIG REQUIRED)
        else()
            find_program(FXC_TOOL fxc REQUIRED)
        endif()
        
        foreach(shaderSource ${_SHADERS_DX11})
            string(REGEX REPLACE "h$" ".h" shaderOutput ${shaderSource})
            if(${shaderSource} MATCHES ".*psh$")
                set(SHADER_TARGET "/Tps_5_0")
            elseif(${shaderSource} MATCHES ".*vsh$")
                set(SHADER_TARGET "/Tvs_5_0")
            else()
                set(SHADER_TARGET "/Tcs_5_0")
            endif()
            add_custom_command(
                OUTPUT ${GENERATED_SOURCES_DIR}/${shaderOutput}
                COMMAND ${CMAKE_COMMAND} -E make_directory ${GENERATED_SOURCES_DIR}/Shaders.metal
                COMMAND ${FXC_TOOL} /nologo ${SHADER_TARGET} /Fo ${GENERATED_SOURCES_DIR}/${shaderSource}.bin ${CMAKE_CURRENT_SOURCE_DIR}/${shaderSource} 
                COMMAND python ${CMAKE_CURRENT_SOURCE_DIR}/bin2h.cmd ${GENERATED_SOURCES_DIR}/${shaderSource}.bin ${GENERATED_SOURCES_DIR}/${shaderOutput}
                MAIN_DEPENDENCY ${shaderSource}
            )
        endforeach()
    endif()

    if (BUILD_DX12)
        ccp_add_executable(TrinityALTest_dx12 ${_SOURCES})
        target_link_libraries(TrinityALTest_dx12 PRIVATE TrinityAL_dx12)
        target_compile_definitions(TrinityALTest_dx12 PRIVATE TRINITY_PLATFORM=TRINITY_DIRECTX12)
        set_shared_trinityaltest_properties(TrinityALTest_dx12)

        # Copy DLL dependencies
        add_custom_command(
            TARGET TrinityALTest_dx12 POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy_if_different $<TARGET_RUNTIME_DLLS:TrinityALTest_dx12> $<TARGET_FILE_DIR:TrinityALTest_dx12>
            COMMAND_EXPAND_LISTS
        )

        target_sources(TrinityALTest_dx12 PRIVATE ${_SHADERS_DX12})
        source_group(Shaders FILES ${_SHADERS_DX12})

        if(BUILD_FOR_PYTHON_2)
            find_package(dxc CONFIG REQUIRED)
            set(DIRECTX_DXC_TOOL ${dxc_ROOT}/bin/${CCP_VENDOR_ARCH_PREFIX}/dxc.exe)
            find_package(fxc CONFIG REQUIRED)
        else()
            find_package(directx-dxc CONFIG REQUIRED)
            find_program(FXC_TOOL fxc REQUIRED)
        endif()
        
        foreach(shaderSource ${_SHADERS_DX12})
            string(REGEX REPLACE "h$" ".h" shaderOutput ${shaderSource})
            set(FXC "${FXC_TOOL}")
            if(${shaderSource} MATCHES ".*psh$")
                set(SHADER_TARGET "/Tps_5_0")
            elseif(${shaderSource} MATCHES ".*vsh$")
                set(SHADER_TARGET "/Tvs_5_0")
            elseif(${shaderSource} MATCHES ".*csh$")
                set(SHADER_TARGET "/Tcs_5_0")
            else()
                set(FXC "${DIRECTX_DXC_TOOL}")
                set(SHADER_TARGET "/Tlib_6_3")
            endif()
            add_custom_command(
                OUTPUT ${GENERATED_SOURCES_DIR}/${shaderOutput}
                COMMAND ${CMAKE_COMMAND} -E make_directory ${GENERATED_SOURCES_DIR}/Shaders.metal
                COMMAND ${FXC} /nologo ${SHADER_TARGET} /Fo ${GENERATED_SOURCES_DIR}/${shaderSource}.bin ${CMAKE_CURRENT_SOURCE_DIR}/${shaderSource} 
                COMMAND python ${CMAKE_CURRENT_SOURCE_DIR}/bin2h.cmd ${GENERATED_SOURCES_DIR}/${shaderSource}.bin ${GENERATED_SOURCES_DIR}/${shaderOutput}
                MAIN_DEPENDENCY ${shaderSource}
            )
        endforeach()

        #GTest
        set_target_properties(TrinityALTest_dx12 PROPERTIES FOLDER "Tests")
        #gtest_discover_tests(TrinityALTest_dx12 myListOfTests)

    endif()

endif()



if(APPLE AND BUILD_METAL)
    ccp_add_executable(TrinityALTest_metal ${_SOURCES})
    target_link_libraries(TrinityALTest_metal PRIVATE TrinityAL_metal)
    target_compile_definitions(TrinityALTest_metal PRIVATE TRINITY_PLATFORM=TRINITY_METAL)
    set_shared_trinityaltest_properties(TrinityALTest_metal)

    set_target_properties(TrinityALTest_metal PROPERTIES FOLDER "Tests")

    # The shader sources are compiled by the custom commands below, never by the
    # compiler driver, and MetalDefines.h is only ever #included by them.
    set(_SHADER_SOURCES_METAL ${_SHADERS_METAL})
    list(FILTER _SHADER_SOURCES_METAL EXCLUDE REGEX "\\.h$")

    target_sources(TrinityALTest_metal PRIVATE ${_SHADERS_METAL})
    source_group(Shaders FILES ${_SHADERS_METAL})
    set_source_files_properties(${_SHADERS_METAL} PROPERTIES HEADER_FILE_ONLY ON)

    # The Metal compiler ships as a separately downloaded toolchain whose install
    # path is a versioned cryptex mount, so it is resolved through xcrun rather
    # than looked up on PATH.
    find_program(XCRUN_TOOL xcrun REQUIRED)
    execute_process(
        COMMAND ${XCRUN_TOOL} -sdk macosx -f metal
        OUTPUT_VARIABLE METAL_TOOL
        OUTPUT_STRIP_TRAILING_WHITESPACE
        RESULT_VARIABLE _METAL_LOOKUP_RESULT
        ERROR_QUIET
    )
    if(NOT _METAL_LOOKUP_RESULT EQUAL 0 OR NOT EXISTS ${METAL_TOOL})
        message(FATAL_ERROR
            "The Metal compiler was not found. Install it with:\n"
            "  xcodebuild -downloadComponent MetalToolchain")
    endif()
    message(STATUS "Using Metal compiler at ${METAL_TOOL}")

    find_package(Python3 COMPONENTS Interpreter REQUIRED)

    set(_GENERATED_SHADER_HEADERS_METAL)
    foreach(shaderSource ${_SHADER_SOURCES_METAL})
        string(REGEX REPLACE "h$" ".h" shaderOutput ${shaderSource})
        add_custom_command(
            OUTPUT ${GENERATED_SOURCES_DIR}/${shaderOutput}
            COMMAND ${CMAKE_COMMAND} -E make_directory ${GENERATED_SOURCES_DIR}/Shaders.metal
            COMMAND ${METAL_TOOL} -x metal
                    -I ${CMAKE_CURRENT_SOURCE_DIR}/Shaders.metal
                    -o ${GENERATED_SOURCES_DIR}/${shaderSource}.metallib
                    ${CMAKE_CURRENT_SOURCE_DIR}/${shaderSource}
            COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/bin2h.cmd
                    ${GENERATED_SOURCES_DIR}/${shaderSource}.metallib
                    ${GENERATED_SOURCES_DIR}/${shaderOutput}
            DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${shaderSource}
                    ${CMAKE_CURRENT_SOURCE_DIR}/Shaders.metal/MetalDefines.h
            COMMENT "Compiling Metal shader ${shaderSource}"
        )
        list(APPEND _GENERATED_SHADER_HEADERS_METAL ${GENERATED_SOURCES_DIR}/${shaderOutput})
    endforeach()

    # The generated headers are #included by the test sources, so they have to
    # exist before anything in the target is compiled.
    add_custom_target(TrinityALTest_metal_shaders DEPENDS ${_GENERATED_SHADER_HEADERS_METAL})
    add_dependencies(TrinityALTest_metal TrinityALTest_metal_shaders)
endif()
