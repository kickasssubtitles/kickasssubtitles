<?php

declare(strict_types=1);

/*
 * KickAssSubtitles source code file
 *
 * @link      https://kickasssubtitles.com
 * @copyright Copyright (c) 2016-2020
 * @author    grzesw <contact@kickasssubtitles.com>
 */

/*
 * healthcheck routes
 ******************************************************************************/

$router
    ->get('healthcheck/cache', 'HealthcheckController@cache')
;
