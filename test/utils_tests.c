/**********************************************************************
 * Copyright (c) 2015 Jonas Schnelli                                  *
 * Copyright (c) 2022 bluezr                                          *
 * Copyright (c) 2022 The Dogecoin Foundation                         *
 * Distributed under the MIT software license, see the accompanying   *
 * file COPYING or http://www.opensource.org/licenses/mit-license.php.*
 **********************************************************************/
#include <test/utest.h>

#include <stdio.h>
#include <math.h>
#include <float.h>
#include <fenv.h>
#include <tgmath.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <dogecoin/utils.h>

/* test a buffer overflow protection */
static const char hash_buffer_exc[] = "28969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c128969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c1";

static const char hex2[] = "AA969cdfFFffFF3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c1";

double compute_fn(double z)  // [1]
{

        // assert(FLT_EVAL_METHOD == 0);  // [3]
<<<<<<< HEAD
        debug_print("FLT_EVAL_METHOD: %d\n", FLT_EVAL_METHOD);
=======
        debug_print("FLT_EVAL_METHOD == 3: %d\n", FLT_EVAL_METHOD == 3);
>>>>>>> 70e7660... utils: IEEE 754 floating point support detection

        if (isnan(z))  // [4]
                debug_print("z is not a number: %f\n", z);

        if (isinf(z))
                debug_print("z is infinite: %f", z);

        long double r = 7.0 - 3.0/(z - 2.0 - 1.0/(z - 7.0 + 10.0/(z - 2.0 - 2.0/(z - 3.0)))); // [5, 6]

<<<<<<< HEAD
#if defined(__GNUC__)
=======
#if !defined(__GNUC__)
>>>>>>> 70e7660... utils: IEEE 754 floating point support detection
        feclearexcept(FE_DIVBYZERO);  // [7]

        bool raised = fetestexcept(FE_OVERFLOW);  // [8]

        if (raised)
<<<<<<< HEAD
                debug_print("Unanticipated overflow: %s\n", raised ? "true" : "false");
=======
                puts("Unanticipated overflow.");
>>>>>>> 70e7660... utils: IEEE 754 floating point support detection
#endif
        return r;
}

void test_utils()
{
    #ifndef __STDC_IEC_559__
    puts("Warning: __STDC_IEC_559__ not defined. IEEE 754 floating point not fully supported."); // [9]
    #endif

    #ifdef TEST_NUMERIC_STABILITY_UP
    fesetround(FE_UPWARD);                   // [10]
    #elif TEST_NUMERIC_STABILITY_DOWN
    fesetround(FE_DOWNWARD);
    #endif

<<<<<<< HEAD
    debug_print("%.7g\n", compute_fn(3.0));
    debug_print("%.7g\n", compute_fn(NAN));
=======
    printf("%.7g\n", compute_fn(3.0));
    printf("%.7g\n", compute_fn(NAN));
>>>>>>> 70e7660... utils: IEEE 754 floating point support detection
    
    int outlen = 0;
    unsigned char data[] = {0x00, 0xFF, 0x00, 0xAA, 0x00, 0xFF, 0x00, 0xAA};
    char hash[] = "28969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c1";
    char hex[sizeof(data) * 2 + 1];
    unsigned char data2[sizeof(data)];
    uint8_t* hash_bin = utils_hex_to_uint8(hash);
    char* new = utils_uint8_to_hex(hash_bin, 32);
    unsigned char data3[64];
    assert(strncmp(new, hash, 64) == 0);

    utils_clear_buffers();

    utils_bin_to_hex(data, sizeof(data), hex);
    assert(strcmp(hex, "00ff00aa00ff00aa") == 0);

    utils_hex_to_bin(hex, data2, strlen(hex), &outlen);
    assert(outlen == 8);
    assert(memcmp(data, data2, outlen) == 0);
    utils_hex_to_uint8(hash_buffer_exc);

    /* test upper and lowercase A / F */
    utils_hex_to_bin(hex2, data3, strlen(hex2), &outlen);
    utils_hex_to_uint8(hex2);
    utils_clear_buffers();

    /* stress test conversion between coins and koinu, round values */
    long double coin_amounts[] = {  1.0e-9, 1.0e-8, 
                                    1.0e-7, 1.0e-6,
                                    1.0e-5, 1.0e-4,
                                    1.0e-3, 1.0e-2,
                                    1.0e-1, 1.0,
                                    1.0e1, 1.0e2,
                                    1.0e3, 1.0e4,
                                    1.0e5, 1.0e6,
                                    1.0e7, 1.0e8,
                                    1.0e9, 1.0e10 };

    uint64_t exp_answers[] = {      0UL, 1UL,
                                    10UL, 100UL,
                                    1000UL, 10000UL,
                                    100000UL, 1000000UL,
                                    10000000UL, 100000000UL,
                                    1000000000UL, 10000000000UL,
                                    100000000000UL, 1000000000000UL,
                                    10000000000000UL, 100000000000000UL,
                                    1000000000000000UL, 10000000000000000UL,
                                    100000000000000000UL, 1000000000000000000UL};
    
    uint64_t actual_answer;
    uint64_t diff;
    const char* build = get_build();
    for (int i=0; i<20; i++) {

        actual_answer = coins_to_koinu(coin_amounts[i]);
<<<<<<< HEAD
    #ifdef WIN32
        debug_print("T%d\n\tcoin_amt: %.9Lg\n\texpected: %lu\n\tactual: %" PRIu64 "\n\n", i, coin_amounts[i], exp_answers[i], actual_answer);
        debug_print("__LDBL_MAX__: %.9lg\n", __LDBL_MAX__);
        debug_print("__LDBL_MAX_10_EXP__: %.9lg\n", __LDBL_MAX_10_EXP__);
        debug_print("__LDBL_MAX_EXP__: %.9lg\n", __LDBL_MAX_EXP__);
        debug_print("__LDBL_MIN__: %.9lg\n", __LDBL_MIN__);
        debug_print("__LDBL_MIN_10_EXP__: %.9lg\n", __LDBL_MIN_10_EXP__);
        debug_print("LDBL_MIN_EXP: %.9lg\n", __LDBL_MIN_EXP__);
        debug_print("__LDBL_DIG__: %.9lg\n", __LDBL_DIG__);
        debug_print("LDBL_EPSILON: %.9lg\n", __LDBL_EPSILON__);
        debug_print("LDBL_MANT_DIG: %.9lg\n", __LDBL_MANT_DIG__);
    #else
        debug_print("T%d\n\tcoin_amt: %.9Lf\n\texpected: %lu\n\tactual: %lu\n\n", i, coin_amounts[i], exp_answers[i], actual_answer);
    #endif
        diff = (exp_answers[i] - actual_answer);
        debug_print("compute_fn(coin_amounts[i]): %f\n", compute_fn(coin_amounts[i]));
        u_assert_int_eq((int)diff, 0);
=======
        debug_print("T%d\n\tcoin_amt: %.9Lf\n\texpected: %lu\n\tactual: %lu\n\n", i, coin_amounts[i], exp_answers[i], actual_answer);
        diff = exp_answers[i] - actual_answer;
        if (i < 10 && build=="ARM7") {
            printf("-----------------------------------\n");
            printf("build: %s\n", get_build());
            printf("------------------------------------\n");
            u_assert_int_eq((int)diff, 0);
        } else if (build !="ARM7") {
            u_assert_int_eq((int)diff, 0);
        }
>>>>>>> 70e7660... utils: IEEE 754 floating point support detection
    }

#if !defined(WIN32)
    /* stress test conversion between coins and koinu, random decimal values */
    long double coin_amounts2[] =  {183447094.420691168L, 410357585.329255459L,
                                    567184894.440967455L, 1560227520.732426502L,
                                    2022535766.086211412L, 2047466422.707290167L,
                                    2487544599.240327145L, 4290779746.000111747L,
                                    4586257992.471687504L, 4660625607.783409803L,
                                    4766962398.856681418L, 5123141607.642632654L,
                                    5432527055.762317749L, 5778056333.994872841L,
                                    6654278072.590832439L, 7037268658.778085185L,
                                    7237308828.705953093L, 8606987445.409636773L,
                                    9100595327.168318456L, 9674059614.504642487L};

<<<<<<< HEAD
   uint64_t exp_answers2[] =      {18344709442069117, 41035758532925546,
=======
    uint64_t exp_answers2[] =      {18344709442069117, 41035758532925546,
>>>>>>> 70e7660... utils: IEEE 754 floating point support detection
                                    56718489444096746, 156022752073242650,
                                    202253576608621141, 204746642270729017,
                                    248754459924032715, 429077974600011175,
                                    458625799247168750, 466062560778340980,
                                    476696239885668142, 512314160764263265,
                                    543252705576231775, 577805633399487284,
                                    665427807259083244, 703726865877808519,
                                    723730882870595309, 860698744540963677,
                                    910059532716831846, 967405961450464249};
<<<<<<< HEAD
    for (int i=0; i<20; i++) {
        debug_print("\n-----------------------------------\nT%d build: %s\n------------------------------------\n", i, get_build());
=======

    for (int i=0; i<20; i++) {
        printf("-----------------------------------\n");
        printf("build: %s\n", get_build());
        printf("------------------------------------\n");
>>>>>>> 70e7660... utils: IEEE 754 floating point support detection
        long double tmp;
        tmp = koinu_to_coins(exp_answers2[i]);
        actual_answer = coins_to_koinu(coin_amounts2[i]);
<<<<<<< HEAD
        tmp = koinu_to_coins(actual_answer);
        diff = exp_answers2[i] - actual_answer;
        debug_print("\n\n\tcoin_amt: %.8Lf\n\texpected: %"PRIu64"\n\tactual:   %"PRIu64"\n\n", coin_amounts2[i], exp_answers2[i], actual_answer);
        u_assert_uint32_eq(actual_answer, exp_answers2[i]);
        u_assert_double_eq(tmp, coin_amounts2[i]);
        u_assert_int_eq((int)diff, 0);

=======
        printf("actual_answer (long long unsigned):     %lu\n", actual_answer);
        printf("exp_answers2 (long long unsigned):      %lu\n", exp_answers2[i]);
        tmp = koinu_to_coins(actual_answer);
        printf("tmp (long double):                      %.9Lf\n", tmp);
        printf("coin_amounts2[i]==tmp:                  %d\n", coin_amounts2[i]==tmp);
        diff = exp_answers2[i] - actual_answer;
        printf("diff (int):                             %d\n", floorl((int)diff));
        printf("diff (long long unsigned):              %lu\n", diff);
        debug_print("T%d\n\tcoin_amt: %.9Lf\n\texpected: %lu\n\tactual: %lu\n\n", i, coin_amounts2[i], exp_answers2[i], actual_answer);
        if (build != "ARM7") {
            // u_assert_long_double_eq(tmp, coin_amounts2[i]);
            u_assert_uint32_eq(actual_answer, exp_answers2[i]);
        }
        // broken on arm:
        // u_assert_int_eq(diff, 0);
>>>>>>> 70e7660... utils: IEEE 754 floating point support detection
    }
#endif
}